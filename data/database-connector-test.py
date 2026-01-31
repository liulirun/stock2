import mysql.connector
from credential import cred


class TestDBConnector:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            host=cred.mysqlDB["url"],
            user=cred.mysqlDB["user"],
            port=3306,
            database="stock",
            charset="utf8",
            use_unicode=True,
            password=cred.mysqlDB["password"],
        )
        self.cur = self.cnx.cursor()

    def __del__(self):
        self.cnx.close()

    def test_db_connection(self):
        _query = "SELECT CURDATE()"
        self.cur.execute(_query)
        row = self.cur.fetchone()
        print("Current date is: {0}".format(row[0]))

    def describe_table(self, table_name):
        _query = f"DESCRIBE stock.{table_name}"
        self.cur.execute(_query)
        row = self.cur.fetchall()
        print(f"Table: {row}")

    def exists_table(self, table_name):
        _query = "SHOW TABLES LIKE '{}';".format(table_name)
        self.cur.execute(_query)
        row = self.cur.fetchall()
        if len(row) == 1:
            print(f" {table_name} exists")
        else:
            print(f" {table_name} not exists")

    def select_from_table(self, table_name, order="DESC"):
        _query = f"SELECT stock_date FROM stock.{table_name} ORDER BY stock_date {order} LIMIT 1;"
        self.cur.execute(_query)
        row = self.cur.fetchone()
        print(f"Table: {row}")

    def select_all_tables(self):
        _query = "SHOW TABLES;"
        self.cur.execute(_query)
        row = self.cur.fetchall()
        assert len(row) > 1
        print(f"Table: {row}")

    def select_from_table_cn_name(self):
        _query = f"SELECT * FROM stock.cn_name;"
        self.cur.execute(_query)
        row = self.cur.fetchall()
        print(f"Table: {row}")

    def select_index_from_table(self, table):
        query = f"SHOW INDEX FROM {table};"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        print(rows)


if __name__ == "__main__":
    conn = TestDBConnector()
    # conn.select_index_from_table(table="US_BABA")
    conn.select_from_table(table_name="US_BABA", order="DESC")
    conn.select_from_table(table_name="US_BABA", order="ASC")

    # conn.create_index_on_stock_date(table="US_BABA", row="stock_date")
    # conn.exists_table(table_name="US_INDEX")
    # conn.exists_table(table_name="US_INDEX1")
    # conn.test_db_connection()

    # conn.describe_table(table_name="US_INDEX")

    # conn.select_from_table_cn_name()
