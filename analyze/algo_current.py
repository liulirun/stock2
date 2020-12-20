from analyze.draw import Draw
from data.db_helper import DbHelper


class Current:
    """
    Current analyze for current date
    """

    def __init__(self):
        self.IF_DEBUG = True
        self.db_helper = DbHelper()

    def run(self, market="US"):
        tables = self.db_helper.get_all_tables()

        #remove TEST table
        if 'TEST' in tables:
            tables.remove('TEST')
            
        table_list = [i for i in tables if i.startswith(market)]
        for i in table_list:
            self.current_stock_data(i)

    def current_stock_data(self, table_name):
        result = self.db_helper.current_stock_data(table_name)
        stock_tuple = result[::-1]
        draw_png = Draw(table_name, stock_tuple)
        draw_png.run()


if __name__ == "__main__":
    c = Current()
    # c.current_stock_data("US_QQQ")
    c.current_stock_data("CN_QQQ")
