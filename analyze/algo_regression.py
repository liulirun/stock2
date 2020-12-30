import math
from operator import methodcaller

from data.db_helper import DbHelper


class Algo_Regression:
    """
    buy_options_and, sell_options_and: all conditions have to be met
    buy_options_or,  sell_options_or:  one condition have to be met
    """

    def __init__(self, stock_name, buy_options_and, buy_options_or, sell_options_and, sell_options_or, start_date):
        self.IF_DEBUG = True
        self.stock_name = stock_name
        self.buy_options_and = list(map(methodcaller("split", "_"), buy_options_and))
        self.buy_options_or = list(map(methodcaller("split", "_"), buy_options_or))
        self.sell_options_and = list(map(methodcaller("split", "_"), sell_options_and))
        self.sell_options_or = list(map(methodcaller("split", "_"), sell_options_or))
        self.buy_methods_and = []
        self.buy_methods_or = []
        self.sell_methods_and = []
        self.sell_methods_or = []

        self.stock_tuple = DbHelper().stock_data_since_date(self.stock_name, start_date)
        self.dates = [str(t[0]) for t in self.stock_tuple]
        self.prices = [float(t[1]) for t in self.stock_tuple]
        self.vols = [int(t[2]) for t in self.stock_tuple]
        self.ma3 = [float(t[3]) for t in self.stock_tuple]
        self.ma13 = [float(t[4]) for t in self.stock_tuple]
        self.ma34 = [float(t[5]) for t in self.stock_tuple]
        self.bulls = [t[6] for t in self.stock_tuple]
        self.zeros = [0 for i in range(len(self.dates))]

        self.index_name = 'US_INDEX' if self.stock_name.startswith('US') else 'CN_INDEX'
        self.index_tuple = DbHelper().stock_data_since_date(self.index_name, start_date)
        self.index_dates_pre = [str(t[0]) for t in self.index_tuple]
        self.index_bulls_pre = [t[6] for t in self.index_tuple]
        self.indexdates = [self.index_dates_pre[index]
                           for index in range(len(self.index_dates_pre)) if self.index_dates_pre[index] in self.dates]
        self.indexbulls = [self.index_bulls_pre[self.index_dates_pre.index(item)] for item in self.indexdates]
        assert self.dates == self.indexdates
        assert len(self.indexbulls) == len(self.indexdates)

        self._money = 10000
        self._stock_amount = 0
        self._if_all_stock = False
        self._transactions = 0
        self._lose_per_transaction = 0.02
        self._dealer_fee = 10

    def individual_stock(self):
        print(
            "Algo_Regression().individual_stock() --> {} since {}".format(self.stock_name, self.dates[0]))
        self.map_options_to_methods()

        for index_i in range(len(self.dates)):
            if (not self._if_all_stock):
                if self._should(index_i, self.buy_methods_and, self.buy_methods_or):
                    self._buy(index_i)
            if (self._if_all_stock):
                if self._should(index_i, self.sell_methods_and, self.sell_methods_or):
                    self._sell(index_i)
        print(
            "Algo_Regression() --> {} since {} for {} days, hold stock today: {}, deals {} times, worth ${}, buy_and_hold would be: ${}\n".format(self.stock_name, self.dates[0], len(self.dates), self._if_all_stock, self._transactions, "{:.2f}".format(self._money + self._stock_amount*self.prices[-1]), "{:.2f}".format(self.prices[-1]*10000/self.prices[0])))

    def _should(self, i, methods_and, methods_or):
        if (methods_and == [] and methods_or == []):
            return False
        for method_list in methods_and:
            # use python eval to run func using parameter from string form in methods.
            if (not eval("{}({},{},{},{})".format(method_list[1], i, method_list[0], method_list[2], method_list[3]))):
                return False
        if methods_or == []:
            return True
        for method_list in methods_or:
            if (eval("{}({},{},{},{})".format(method_list[1], i, method_list[0], method_list[2], method_list[3]))):
                return True
        return False

    def _buy(self, i):
        _price = self.prices[i] * (1 + self._lose_per_transaction)
        if self._money > self._dealer_fee + _price:
            self._stock_amount = math.floor((self._money - self._dealer_fee)/_price)
            self._money = self._money - self._stock_amount*_price
            self._if_all_stock = True
            self._transactions += 1
            if self.IF_DEBUG:
                print("  --BUY  at {}, price {}, for {} stocks, money left {}".format(
                    self.dates[i], "{:.2f}".format(_price), self._stock_amount, "{:.2f}".format(self._money)))

    def _sell(self, i):
        _price = self.prices[i] * (1 - self._lose_per_transaction)
        if self._stock_amount >= 1:
            self._money = self._money + self._stock_amount * _price - self._dealer_fee
            self._stock_amount = 0
            self._if_all_stock = False
            if self.IF_DEBUG:
                print("  --SELL at {}, price {}, money got {}".format(
                    self.dates[i], "{:.2f}".format(_price), "{:.2f}".format(self._money)))

    def greaterthan(self, index, list_a, list_b, percentage=0):
        return list_a[index] > list_b[index]*(1+percentage/100)

    def lessthan(self, i, list_a, list_b, percentage=0):
        return list_a[i] <= list_b[i]*(1-percentage/100)

    def map_options_to_methods(self):
        """
        use python map to get func and parameter methods from options which is in string form
        """
        if len(self.buy_options_and) > 0:
            print("  BUY_option_and:  {}".format(self.buy_options_and))
        if len(self.buy_options_or) > 0:
            print("  BUY_option_or:   {}".format(self.buy_options_or))
        if len(self.sell_options_and) > 0:
            print("  SELL_option_and: {}".format(self.sell_options_and))
        if len(self.sell_options_or) > 0:
            print("  SELL_option_or:  {}".format(self.sell_options_or))

        for temp_list in self.buy_options_and:
            self.buy_methods_and.append([int(s) if s.isdigit() else 'self.'+s for s in temp_list])
        for temp_list in self.buy_options_or:
            self.buy_methods_or.append([int(s) if s.isdigit() else 'self.'+s for s in temp_list])
        for temp_list in self.sell_options_and:
            self.sell_methods_and.append([int(s) if s.isdigit() else 'self.'+s for s in temp_list])
        for temp_list in self.sell_options_or:
            self.sell_methods_or.append([int(s) if s.isdigit() else 'self.'+s for s in temp_list])


def run(market="US", start_date='2013-12-01'):
    db_helper = DbHelper()
    tables = db_helper.get_all_tables()

    tables.remove('cn_names')  # remove TEST table
    if 'TEST' in tables:
        tables.remove('TEST')

    table_list = [i for i in tables if i.startswith(market)]
    options_lists = [
        [["ma3_greaterthan_ma13_10", "bulls_greaterthan_zeros_0", "prices_greaterthan_ma3_10"],
            [], [], ["ma13_lessthan_ma34_10", "bulls_lessthan_zeros_0"]],  # regression 1
        [["bulls_greaterthan_zeros_0"], [], ["bulls_lessthan_zeros_0"], []],  # regression 2
        [["bulls_greaterthan_zeros_0", "prices_lessthan_ma3_10"],
            [], [], ["prices_greaterthan_ma3_10", "bulls_lessthan_zeros_0"]],  # regression 3
        [["bulls_greaterthan_zeros_0", "prices_lessthan_ma3_15"],
            [], [], ["prices_greaterthan_ma3_15"]],  # regression 4
    ]

    for i in table_list:
        for option_list in options_lists:
            d = Algo_Regression(i,
                                buy_options_and=option_list[0],
                                buy_options_or=option_list[1],
                                sell_options_and=option_list[2],
                                sell_options_or=option_list[3],
                                start_date=start_date
                                )
            d.individual_stock()


def regression_dryrun(stock_name, start_date='2010-01-01'):
    options_lists = [

        [["bulls_greaterthan_zeros_0", "indexbulls_greaterthan_zeros_0"],
            [], ["bulls_lessthan_zeros_0", "indexbulls_lessthan_zeros_0"], []],
        [["bulls_greaterthan_zeros_0", "indexbulls_greaterthan_zeros_0"],
            [], ["indexbulls_lessthan_zeros_0"], []],
        # [["bulls_greaterthan_zeros_0", "prices_greaterthan_ma34_1"],
        #     [], [], ["prices_lessthan_ma34_1"]],
        # [["bulls_greaterthan_zeros_0", "prices_greaterthan_ma34_2"],
        #     [], [], ["prices_lessthan_ma34_2"]],
        # [["bulls_greaterthan_zeros_0", "prices_greaterthan_ma34_5"],
        #     [], [], ["prices_lessthan_ma34_5"]],
    ]

    for option_list in options_lists:
        d = Algo_Regression(stock_name,
                            buy_options_and=option_list[0],
                            buy_options_or=option_list[1],
                            sell_options_and=option_list[2],
                            sell_options_or=option_list[3],
                            start_date=start_date
                            )
        d.individual_stock()


if __name__ == "__main__":
    regression_dryrun('US_TDOC', '2018-01-01')
    regression_dryrun('US_TSLA', '2018-01-01')
    regression_dryrun('US_PDD', '2018-01-01')
    regression_dryrun('US_SQ', '2018-01-01')
