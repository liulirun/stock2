import math
from datetime import date
from operator import methodcaller

import matplotlib
import numpy as np
from matplotlib import gridspec, pyplot

from data.db_helper import DbHelper

matplotlib.use('Agg')


class Algo_Regression:
    """
    buy_options_and, sell_options_and: all conditions have to be met
    buy_options_or,  sell_options_or:  one condition have to be met
    """

    def __init__(self, stock_name, buy_options_and, buy_options_or, sell_options_and, sell_options_or, start_date, end_date, cn_name=''):
        self.IF_DEBUG = False
        self.top_n = 10
        self.stock_name = stock_name
        self.cn_name = cn_name
        self.buy_options_and = list(map(methodcaller("split", "_"), buy_options_and))
        self.buy_options_or = list(map(methodcaller("split", "_"), buy_options_or))
        self.sell_options_and = list(map(methodcaller("split", "_"), sell_options_and))
        self.sell_options_or = list(map(methodcaller("split", "_"), sell_options_or))
        self.buy_methods_and = []
        self.buy_methods_or = []
        self.sell_methods_and = []
        self.sell_methods_or = []

        self.stock_tuple = DbHelper().stock_data_since_date(self.stock_name, start_date, end_date)
        self.dates = [str(t[0]) for t in self.stock_tuple]
        self.prices = [float(t[1]) for t in self.stock_tuple]
        self.vols = [int(t[2]) for t in self.stock_tuple]
        self.ma3 = [float(t[3]) for t in self.stock_tuple]
        self.ma13 = [float(t[4]) for t in self.stock_tuple]
        self.ma34 = [float(t[5]) for t in self.stock_tuple]
        self.bulls = [t[6] for t in self.stock_tuple]
        self.zeros = [0 for i in range(len(self.dates))]
        self.latest_date = str(self.stock_tuple[-1][0])
        self.min_price = min(self.prices)
        self.max_price = max(self.prices)
        self.option_title = ""

        self.index_name = 'US_INDEX' if self.stock_name.startswith('US') else 'CN_INDEX'
        self.index_tuple = DbHelper().stock_data_since_date(self.index_name, start_date, end_date)
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

        self.subplotcolor = "#cc9918"  # yellow-brown ish
        self.backcolor = "#999a88"  # grey

        params = {'legend.fontsize': 'medium',
                  'legend.title_fontsize': 'x-large',
                  'figure.figsize': (20, 10),
                  'axes.labelsize': 'large',
                  'axes.titlesize': 'large',
                  'axes.facecolor': self.subplotcolor,
                  'figure.facecolor': self.backcolor,
                  'font.family': 'sans-serif',
                  'font.sans-serif': ['Microsoft YaHei'],  # you need to point to a font in C:\Windows\Fonts
                  }
        pyplot.rcParams.update(params)

        self.fig = pyplot.figure()

        grid_specs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1])
        self.price_ax = pyplot.subplot(grid_specs[0])
        self.ma_ax_1 = pyplot.subplot(grid_specs[1])
        self.ma_ax_2 = pyplot.subplot(grid_specs[2])

    def individual_stock(self, index=1):
        if self.IF_DEBUG:
            print("Algo_Regression().individual_stock() --> {} since {}".format(self.stock_name, self.dates[0]))

        self.map_options_to_methods()

        self.price_ax.set_title("{}".format(self.option_title.rstrip()), loc="left")

        self.draw_price(self.price_ax)
        self.draw_ma(self.ma_ax_1, self.ma34, 'orange')  # orange for ma34
        self.draw_ma(self.ma_ax_2, self.ma13, 'blue')  # blue for ma13

        for index_i in range(len(self.dates)):
            if (not self._if_all_stock):
                if self._should(index_i, self.buy_methods_and, self.buy_methods_or):
                    self._buy(index_i)
            if (self._if_all_stock):
                if self._should(index_i, self.sell_methods_and, self.sell_methods_or):
                    self._sell(index_i)

        _money = "{:.2f}".format(self._money + self._stock_amount*self.prices[-1])
        _hold = "{:.2f}".format(self.prices[-1]*10000/self.prices[0])
        _percent = int(float(_money)*100/float(_hold))
        print(
            "\n\n{} for {} days\n  still has stock today: {}\tdeals {} times\n  strategy ${}\tbuy_hold ${}\tstrategy/buy_hold:{} times"
            .format(self.stock_name, len(self.dates), self._if_all_stock, self._transactions, _money, _hold, _percent/100))
        self.price_ax.set_title("start:$10000.00\nstrategy:${}\nbuy_hold:${}\nstrategy/buy_hold:{}%".format(_money, _hold, _percent), loc="right")
        self.save_png(index)

    def _should(self, i, methods_and, methods_or):
        if (methods_and == [] and methods_or == []):
            return False
        for method_list in methods_and:
            # use python eval to  func using parameter from string form in methods.
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
            self.price_ax.axvline(x=i, ymin=0, ymax=_price/self.max_price, linewidth=1, color='green')
            self.ma_ax_1.axvline(x=i, ymin=0, ymax=1, linewidth=1, color='green')
            self.ma_ax_2.axvline(x=i, ymin=0, ymax=1, linewidth=1, color='green')
            # pyplot.text(i, self.min_price, "{}".format(_price), weight='bold', c='g')
            if self.IF_DEBUG:
                print("  --BUY  at {}, price {}, for {} stocks, money left {}".format(
                    self.dates[i], "{:.2f}".format(_price), self._stock_amount, "{:.2f}".format(self._money)))

    def _sell(self, i):
        _price = self.prices[i] * (1 - self._lose_per_transaction)
        if self._stock_amount >= 1:
            self._money = self._money + self._stock_amount * _price - self._dealer_fee
            self._stock_amount = 0
            self._if_all_stock = False
            self.price_ax.axvline(x=i, ymin=0, ymax=_price/self.max_price, linewidth=1, color='red')
            self.price_ax.text(i, self.max_price, "${:.2f}".format(self._money), weight='bold', c='black')
            self.ma_ax_1.axvline(x=i, ymin=0, ymax=1, linewidth=1, color='red')
            self.ma_ax_2.axvline(x=i, ymin=0, ymax=1, linewidth=1, color='red')
            if self.IF_DEBUG:
                print("  --SELL at {}, price {}, money got {}".format(
                    self.dates[i], "{:.2f}".format(_price), "{:.2f}".format(self._money)))

    def greaterthan(self, index, list_a, list_b, percentage=0):
        return list_a[index] > list_b[index]*(1+percentage/100)

    def lessthan(self, i, list_a, list_b, percentage=0):
        return list_a[i] <= list_b[i]*(1-percentage/100)

    def draw_price(self, ax):
        ax.set_title("{}{} - {}".format(self.stock_name, self.cn_name, self.latest_date))
        ax.plot(self.prices, color='black', label='price')
        ax.plot(self.ma3, color='green', linestyle='dashed', label='ma3')
        ax.plot(self.ma13, color='blue', linestyle='dashed', label='ma13')
        ax.plot(self.ma34, color='red', linestyle='dashed', label='ma34')

        ax.legend(loc='upper left', bbox_to_anchor=[0, 1], shadow=True)

    def draw_ma(self, ax, ma_list, face_color):
        list_len = len(self.prices)
        ar = np.arange(0, list_len, 1)

        diff_list = [(self.prices[i]-ma_list[i])*100/self.prices[i] for i in range(list_len)]

        _diff_sorted = sorted(diff_list)
        _lower = max(_diff_sorted[0: math.ceil(list_len*self.top_n/100)])
        lower_array = np.full((list_len), _lower)
        _higher = min(_diff_sorted[math.floor(list_len*(100-self.top_n)/100):])
        higher_array = np.full((list_len), _higher)
        diff_array = np.array(diff_list)

        ax.set_title('10% of ma_diff')
        ax.xaxis.set_visible(False)
        ax.plot(diff_array, color=face_color)
        ax.text(list_len, _lower, "{:.2f}".format(_lower), fontsize=12)
        ax.text(list_len, _higher, "{:.2f}".format(_higher), fontsize=12)
        ax.fill_between(ar, diff_array, higher_array, where=(diff_array >= higher_array),
                        interpolate=True, facecolor='red', alpha=0.75)
        ax.fill_between(ar, diff_array, lower_array, where=(diff_array <= lower_array),
                        interpolate=True, facecolor='green', alpha=0.75)

    def save_png(self, index):
        pyplot.savefig("./analyze/regression_result/reg_{}_{}.png".format(self.stock_name, index))
        pyplot.close(self.fig)

    def map_options_to_methods(self):
        """
        use python map to get func and parameter methods from options which is in string form
        """
        if len(self.buy_options_and) > 0:
            if self.IF_DEBUG:
                print("  BUY_option_and:  {}".format(self.buy_options_and))
            self.option_title += "BUY_option_and: {}\n".format(self.buy_options_and)
        if len(self.buy_options_or) > 0:
            if self.IF_DEBUG:
                print("  BUY_option_or:   {}".format(self.buy_options_or))
            self.option_title += "BUY_option_or: {}\n".format(self.buy_options_or)
        if len(self.sell_options_and) > 0:
            if self.IF_DEBUG:
                print("  SELL_option_and: {}".format(self.sell_options_and))
            self.option_title += "SELL_option_and: {}\n".format(self.sell_options_and)
        if len(self.sell_options_or) > 0:
            if self.IF_DEBUG:
                print("  SELL_option_or:  {}".format(self.sell_options_or))
            self.option_title += "SELL_option_or: {}\n".format(self.sell_options_or)

        for temp_list in self.buy_options_and:
            self.buy_methods_and.append([int(s) if s.isdigit() else 'self.'+s for s in temp_list])
        for temp_list in self.buy_options_or:
            self.buy_methods_or.append([int(s) if s.isdigit() else 'self.'+s for s in temp_list])
        for temp_list in self.sell_options_and:
            self.sell_methods_and.append([int(s) if s.isdigit() else 'self.'+s for s in temp_list])
        for temp_list in self.sell_options_or:
            self.sell_methods_or.append([int(s) if s.isdigit() else 'self.'+s for s in temp_list])


def combine_run(market="US", start_date='2022-01-01', end_date=date.today()):
    db_helper = DbHelper()
    tables = db_helper.get_all_tables()

    tables.remove('cn_names')  # remove TEST table
    if 'TEST' in tables:
        tables.remove('TEST')

    table_list = [i for i in tables if i.startswith(market)]
    options_lists = [
        [["prices_lessthan_ma34_5", "indexbulls_greaterthan_zeros_0"],
            [], [], ["prices_greaterthan_ma34_20", "indexbulls_lessthan_zeros_0"]],
        [["prices_lessthan_ma34_10", "indexbulls_greaterthan_zeros_0"],
            [], [], ["prices_greaterthan_ma34_25", "indexbulls_lessthan_zeros_0"]],
        [["prices_lessthan_ma13_10", "indexbulls_greaterthan_zeros_0"],
            [], [], ["prices_greaterthan_ma13_15", "indexbulls_lessthan_zeros_0"]],
        [["prices_lessthan_ma13_10", "indexbulls_greaterthan_zeros_0"],
            [], [], ["prices_greaterthan_ma13_20", "indexbulls_lessthan_zeros_0"]],
    ]

    for i in table_list:
        for index, option_list in enumerate(options_lists, start=1):
            d = Algo_Regression(i,
                                buy_options_and=option_list[0],
                                buy_options_or=option_list[1],
                                sell_options_and=option_list[2],
                                sell_options_or=option_list[3],
                                start_date=start_date, 
                                end_date=end_date
                                )
            d.individual_stock(index=index)


def regression_dryrun(stock_name, start_date='2010-01-01', end_date=date.today()):
    options_lists = [
        [["prices_greaterthan_ma34_0"],
            [], [], ["prices_lessthan_ma34_0"]],
    ]

    for index, option_list in enumerate(options_lists, start=1):
        d = Algo_Regression(stock_name,
                            buy_options_and=option_list[0],
                            buy_options_or=option_list[1],
                            sell_options_and=option_list[2],
                            sell_options_or=option_list[3],
                            start_date=start_date,
                            end_date=end_date
                            )
        d.individual_stock(index=index)


if __name__ == "__main__":
    # for i in ['US_NIU']:
    for i in ['US_LABU', 'US_QQQ', 'US_UPST', 'US_PDD', 'US_TSLA', 'US_NIU']:
        # (i, start_date='2022-01-01')
        # regression_dryrun(i, start_date='2020-02-10', end_date='2022-02-20')
        combine_run(i, start_date='2020-02-10', end_date='2022-02-20')
    