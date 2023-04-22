
import matplotlib.pyplot as pyplot
import numpy as np
from matplotlib import gridspec
from scipy.stats import gaussian_kde


class DrawHelper():
    def __init__(self, stock_name, stock_tuple, cn_name='', sub_folder='daily_result'):
        self.IF_DEBUG = False
        self.stock_name = stock_name
        self.cn_name = cn_name
        self.sub_folder = sub_folder
        self.date_list = [str(t[0]) for t in stock_tuple]
        self.price_list = [float(t[1]) for t in stock_tuple]
        self.vol_list = [int(t[2]) for t in stock_tuple]
        self.ma3 = [float(t[3]) for t in stock_tuple]
        self.ma13 = [float(t[4]) for t in stock_tuple]
        self.ma34 = [float(t[5]) for t in stock_tuple]
        self.bull_list = [t[6] for t in stock_tuple]
        self.latest_date = str(stock_tuple[-1][0])
        self.subplotcolor = "#cc9918"  # yellow ish
        self.backcolor = "#999a88"  # grey

    def run(self):
        if self.IF_DEBUG:
            print("  DrawHelper().run() --> start with {}, at {}".format(self.stock_name, self.latest_date))
        params = {'legend.fontsize': 'medium',
                  'legend.title_fontsize': 'x-large',
                  'figure.figsize': (20, 10),
                  'axes.labelsize': 'x-large',
                  'axes.titlesize': 'x-large',
                  'axes.facecolor': self.subplotcolor,
                  'figure.facecolor': self.backcolor,
                  'font.family': 'sans-serif',
                  'font.sans-serif': ['Microsoft YaHei'],  # you need to point to a font in C:\Windows\Fonts
                  }
        pyplot.rcParams.update(params)

        fig = pyplot.figure()
        fig.suptitle("{}{} - {}".format(self.stock_name, self.cn_name, self.latest_date))

        grid_specs = gridspec.GridSpec(3, 2, height_ratios=[2, 2, 1])
        self.draw_kde(grid_specs[0])
        self.draw_price(grid_specs[2], grid_specs[3])
        self.draw_vol(grid_specs[4], grid_specs[5])

        pyplot.savefig(f"./analyze/{self.sub_folder}/{self.stock_name}.png")
        pyplot.close(fig)

        if self.IF_DEBUG:
            print(f"  DrawHelper().run() --> {self.stock_name} saved")

    def draw_price(self, gs_left, gs_right):
        ax1 = pyplot.subplot(gs_left)
        ax1.plot(self.price_list, color='black', label='price')
        ax1.plot(self.ma13, color='blue', label='ma13')
        ax1.plot(self.ma34, color='red', label='ma34')
        ax1.legend(loc='upper left', bbox_to_anchor=[0, 1], shadow=True)

        ax2 = pyplot.subplot(gs_right)
        _bull = 'BULL' if self.bull_list[-1] == 1 else 'BEAR'
        ax2.title.set_text("tick market: {}".format(_bull))

        ax2.plot(self.price_list[-21:], color='black', label='price')
        ax2.plot(self.ma3[-21:], color='green', label='ma3')
        ax2.plot(self.ma13[-21:], color='blue', label='ma13')
        ax2.plot(self.ma34[-21:], color='red', label='ma34')
        # ax2.fill_between(self.price_list[-21:], self.ma3[-21:], color='green')
        leg = ax2.legend(loc='upper left', bbox_to_anchor=[0, 1], title="tick:{}".format(_bull), shadow=True)
        if _bull == 'BEAR':
            leg.get_title().set_color("red")

    def draw_vol(self, gs_left, gs_right):
        ax1 = pyplot.subplot(gs_left)
        ax1.get_yaxis().set_visible(False)
        ax1.get_xaxis().set_visible(False)
        index_list = [i+1 for i in range(len(self.price_list))]
        ax1.bar(index_list, height=self.vol_list, color=self.backcolor)

        ax2 = pyplot.subplot(gs_right)
        ax2.get_yaxis().set_visible(False)
        ax2.get_xaxis().set_visible(False)
        index_list = [i for i in range(21)]
        ax2.bar(index_list, height=self.vol_list[-21:], color=self.backcolor)

    def draw_kde(self, gs_left):
        ax1 = pyplot.subplot(gs_left)
        ax1.title.set_text('2 years gaussian_kde')
        ax1.get_yaxis().set_visible(False)
        money_list = [self.price_list[i]*self.vol_list[i] for i in range(len(self.vol_list))]
        xs = np.linspace(min(self.price_list), max(self.price_list), 400)

        # calc density of 2 years money_list
        density = gaussian_kde(dataset=self.price_list, weights=money_list)
        density.covariance_factor = lambda: .1
        density._compute_covariance()

        ax1.plot(xs, density(xs), color=self.backcolor)
        ax1.scatter(self.price_list[-1], 0.0025, s=50, color='red')


if __name__ == "__main__":
    pass
