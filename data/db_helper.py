import sys
from datetime import date, datetime

import MySQLdb as db

from credential import cred
from data.json_helper import JsonHelper


class DbHelper:
    """
    manipulate Mysql DB
    """

    def __init__(self):
        self.IF_DEBUG = False
        self.cnx = db.connect(
            host=cred.mysqlDB["url"],
            user=cred.mysqlDB["user"],
            password=cred.mysqlDB["password"],
            database='stock',
            charset="utf8",
            use_unicode=True
        )

    def run(self, table_name, CN_name=''):
        """
        entry point to insert stock data
        takes table_name like US_TLSA
        """
        self.create_DB_if_not_exists(table_name)

        stock_name = table_name
        self.insert_stock_CN_names(table_name, CN_name)
        stock_list = self.insert_stock_data_to_db(stock_name)

    def create_DB_if_not_exists(self, table_name):
        if (not self.table_exists(table_name)):
            if self.IF_DEBUG:
                print("  DB table {} not exists, creating now".format(table_name))
            self.create_table(table_name)

    def insert_stock_CN_names(self, table_name, CN_name):
        if (not self.table_exists('cn_names')):
            self.create_cn_name_table('cn_names')

        query = "INSERT INTO stock.cn_names (cn_code, cn_name) SELECT * FROM (SELECT '{}', '{}') AS tmp \
            WHERE NOT EXISTS ( SELECT cn_code FROM stock.cn_names WHERE cn_code='{}') LIMIT 1;".format(table_name, CN_name, table_name)
        self._commit_DB_change(query)

    def _commit_DB_change(self, query):
        """
        for inserting/updating DB
        """
        try:
            _cursor = self.cnx.cursor()
            _cursor.execute(query)
            self.cnx.commit()
            _cursor.close()

        except db.ProgrammingError as err:
            raise ValueError("{}, {}, {}".format(err.errno, err.sqlstate, err.msg))
        except db.Error as err:
            raise ValueError("Oops! {} occurred".format(err))
        except:
            raise ValueError("Oops! {} occurred".format(sys.exc_info()[0]))

    def _read_json(self, stock_name):
        try:
            json_helper = JsonHelper()
            json_dict = json_helper.read_json(stock_name)
            return json_dict
        except:
            raise ValueError("can not read Json file:{}".format(stock_name))

    def _fetch_all(self, query):
        try:
            _cursor = self.cnx.cursor()
            _cursor.execute(query)
            result = _cursor.fetchall()
            return result
        except:
            raise ValueError("Oops! {} occurred".format(sys.exc_info()[0]))

    def _latest_date_in_db(self, stock_name):
        _query = "SELECT stock_date FROM stock.{} ORDER BY stock_date DESC LIMIT 1".format(stock_name)
        result = self._fetch_all(_query)
        if (len(result) == 0):
            return date(2081, 1, 1)
        return result[0][0]

    def truncate_table(self, table_name):
        _query = "TRUNCATE TABLE {};".format(table_name)
        self._commit_DB_change(_query)
        if self.IF_DEBUG:
            print("  truncate_table() --> truncate table {}".format(table_name))

    def drop_table(self, table_name):
        _query = "DROP TABLE {};".format(table_name)
        self._commit_DB_change(_query)

    def create_table(self, table_name):
        """
        bull column, -1:not data, 0: BEAR, 1:BULL
        """
        _query = "CREATE TABLE {} (\
            stock_date date PRIMARY KEY, \
            price decimal(15,2) not null, \
            vol bigint not null, \
            a3 decimal(15,2) not null, \
            a13 decimal(15,2) not null, \
            a34 decimal(15,2) not null, \
            bull tinyint not null, \
            created_by date not null, \
            updated_by date not null\
            );".format(table_name)
        self._commit_DB_change(_query)

    def create_cn_name_table(self, table_name):
        _query = "CREATE TABLE {} (\
            cn_code CHAR(12) PRIMARY KEY, \
            cn_name CHAR(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci not null\
            );".format(table_name)
        self._commit_DB_change(_query)

    def table_exists(self, table_name):
        _query = "SHOW TABLES like '{}';".format(table_name)
        try:
            _cursor = self.cnx.cursor()
            _cursor.execute(_query)
            result = (_cursor.rowcount == 1)
            return result
        except:
            raise ValueError("Oops! {} occurred".format(sys.exc_info()[0]))

    def insert_stock_data_to_db(self, stock_name):
        """
        read json, then generate stock_list
        """
        stock_json = self._read_json(stock_name)
        if (len(stock_json) == 0):
            return []
        dl = stock_json['date']
        pl = stock_json['c']
        vl = stock_json['v']
        m3 = stock_json['3']
        m13 = stock_json['13']
        m34 = stock_json['34']
        bl = stock_json['BULL']
        sl = stock_json['sp']
        ds = str(date.today())
        _index = -1
        json_earliest = datetime.strptime(dl[0], "%Y-%m-%d").date()
        jason_latest = datetime.strptime(dl[-1], "%Y-%m-%d").date()
        # db_latest type is datetime.date
        db_latest = self._latest_date_in_db(stock_name)

        # DB will have gap, do not insert
        if (json_earliest > db_latest):
            raise ValueError("json_earliest:{} greater than db_latest {}, data in DB will have gap".format(
                str(json_earliest), str(db_latest)))

        # Download Json latest is earlier than DB, something wrong with DB, check DB
        if (jason_latest < db_latest and str(db_latest) != "2081-01-01"):
            raise ValueError("jason_latest:{} less than db_latest {}, something wrong with Database".format(
                str(jason_latest), str(db_latest)))

        # DB is the latest, no need to insert
        if (jason_latest == db_latest):
            return []

        # a slice of list
        if (jason_latest > db_latest):
            _index = dl.index(str(db_latest)) + 1

        # no data in DB, insert all
        if (str(db_latest) == "2081-01-01"):
            _index = 0

        if (_index == -1):
            raise ValueError("_index is still -1, check coverage path")

        l_length = len(dl)
        stock_list = [(dl[i], pl[i], vl[i], m3[i], m13[i], m34[i], bl[i], ds, ds) for i in range(_index, l_length)]

        if any(i != 1.0 for i in sl[_index:l_length]):
            self.truncate_table(stock_name)

        if self.IF_DEBUG:
            print("  insert_stock_data_to_db() --> stock_list from {} to {} generated".format(dl[_index], dl[-1]))

        self.insert_tick_data(stock_name, stock_list)
        return stock_list

    def insert_tick_data(self, table_name, stock_list):
        """for individual stock only
        """
        _query = "INSERT INTO stock.{} (stock_date, price, vol, a3, a13, a34, bull, created_by, updated_by) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table_name)
        print("DbHelper().insert_tick_data() --> insert into {} for {} lines".format(table_name, len(stock_list)))

        try:
            _cursor = self.cnx.cursor()
            _cursor.executemany(_query, stock_list)
            self.cnx.commit()
        except:
            raise ValueError("Oops! {} occurred".format(sys.exc_info()[0]))

    def get_all_tables(self):
        _query = "SHOW TABLES;"
        _cursor = self.cnx.cursor()
        _result = _cursor.execute(_query)
        assert _result > 1
        return [i[0] for i in _cursor._rows]

    def stock_data_for_days(self, table_name, days=484):
        _query = "SELECT * FROM stock.{} ORDER BY stock_date DESC LIMIT {};".format(table_name, days)
        result = self._fetch_all(_query)
        return result

    def stock_data_since_date(self, table_name, start_date, end_date=date.today()):
        _query = "SELECT * FROM stock.{} where stock_date >= '{}' and stock_date <= '{}' ORDER BY stock_date ASC;".format(table_name, start_date, end_date)
        result = self._fetch_all(_query)
        return result

    def current_stock_cn_name(self, table_name):
        _query = "SELECT cn_name FROM stock.cn_names WHERE cn_code='{}' LIMIT 1;".format(table_name)
        result = self._fetch_all(_query)
        if len(result) > 0:
            return result[0][0]
        return ''

    def closest_date(self, table_name, start_date):
        _query = "SELECT stock_date from stock.{} where stock_date >= '{}' \
            order by stock_date ASC Limit 1;".format(table_name, start_date)
        result = self._fetch_all(_query)
        assert len(result) > 0
        return result[0][0]


if __name__ == "__main__":
    pass
