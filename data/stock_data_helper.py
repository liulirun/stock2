import pandas as pd


class StockDataHelper:
    """
    [summary]
    generate ma list from json file
    one instance per stock
    """

    def __init__(self):
        self.BULL_INTERVAL = 60

    def _ma_list(self, window_size, price_list):
        numbers_series = pd.Series(price_list)
        windows = numbers_series.rolling(window_size)
        ma_list_pre = windows.mean().tolist()
        ma_list = [i if i > 0 else 0 for i in ma_list_pre]
        assert len(ma_list) == len(price_list), "ERROR: len(ma_list) != len(price_list)"
        return ma_list

    def ma_lists(self, price_list):
        ma_3 = self._ma_list(3, price_list)
        ma_13 = self._ma_list(13, price_list)
        ma_34 = self._ma_list(34, price_list)
        return ma_3, ma_13, ma_34

    def bull_list(self, price_list):
        """in the returned bull_list, -1 means no data because of interval, 0 means BEAR, 1 means BULL
        """
        if (len(price_list) <= self.BULL_INTERVAL):
            return [-1 for i in price_list]

        first_list = [-1 for i in range(0, self.BULL_INTERVAL)]
        #if cur price > price_60_days_ago, then bull
        second_list = [1 if price_list[i] >= price_list[i-self.BULL_INTERVAL]
                       else 0 for i in range(self.BULL_INTERVAL, len(price_list))]
        bull_list = first_list + second_list
        assert len(bull_list) == len(price_list), "ERROR: len(bull_list) != len(price_list)"
        return bull_list


if __name__ == "__main__":
    pass
