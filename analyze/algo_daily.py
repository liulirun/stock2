
from analyze.draw_helper import DrawHelper
from data.db_helper import DbHelper


class Algo_Daily:
    """
    analyze for current date
    """

    def __init__(self):
        self.db_helper = DbHelper()

    def run(self, market="US"):
        tables = self.db_helper.get_all_tables()

        tables.remove('cn_names')
        # remove TEST table
        if 'TEST' in tables:
            tables.remove('TEST')

        table_list = [i for i in tables if i.startswith(market)]
        for i in table_list:
            print("Algo_Daily().run() --> for {}".format(i))
            self.draw_stock_data(table_name=i, days=484)

    def draw_stock_data(self, table_name, days):
        result = self.db_helper.stock_data_for_days(table_name=table_name, days=days)
        stock_tuple = result[::-1]
        cn_name = self.db_helper.current_stock_cn_name(table_name)

        draw_png = DrawHelper(table_name, stock_tuple, cn_name, "daily_result")
        draw_png.run()


if __name__ == "__main__":
    pass
