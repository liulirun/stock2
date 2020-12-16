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
        self.IF_DEBUG = True
        self.cnx = db.connect(
            host=cred.mysqlDB["url"],
            user=cred.mysqlDB["user"],
            password=cred.mysqlDB["password"],
            database='stock'
        )

    def run(self, table_name):
        """
        entry point to insert stock data
        takes table_name like US_TLSA
        """
        if self.IF_DEBUG:
            print("start DbHelper.run() for table_name: {}".format(table_name))

        if (not self.table_exists(table_name)):
            if self.IF_DEBUG:
                print("  DB table {} not exists, creating now".format(table_name))
            self.create_table(table_name)

        if (self.table_exists(table_name)):
            stock_name = table_name
            stock_list = self.insert_stock_data_to_db(stock_name)

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
            json_dict = JsonHelper().read_json(stock_name)
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

        stock_list = [(dl[i], pl[i], vl[i], m3[i], m13[i], m34[i], bl[i], ds, ds) for i in range(_index, len(dl))]
        if self.IF_DEBUG:
            print("  insert_stock_data_to_db() --> stock_list from {} to {} generated".format(dl[_index], dl[-1]))
        self.insert_tick_data(stock_name, stock_list)
        return stock_list

    def insert_tick_data(self, table_name, stock_list):
        """for individual stock only
        """
        _query = "INSERT INTO stock.{} (stock_date, price, vol, a3, a13, a34, bull, created_by, updated_by) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table_name)
        if self.IF_DEBUG:
            print("  insert_tick_data() --> insert into {} for {} lines".format(table_name, len(stock_list)))

        try:
            _cursor = self.cnx.cursor()
            _cursor.executemany(_query, stock_list)
            self.cnx.commit()
        except:
            raise ValueError("Oops! {} occurred".format(sys.exc_info()[0]))


if __name__ == "__main__":
    pass
