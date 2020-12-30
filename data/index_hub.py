from time import time

import requests
from data.json_helper import JsonHelper
from data.stock_data_helper import StockDataHelper


class Indexhub:
    def __init__(self, market, start_timestamp=1261612800, end_timestamp=int(time())):
        self.IF_DEBUG = False
        self.market = market
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp

    def run(self):
        index_bytes = self.download_candle()
        stock_dict = self.convert_candle_data(index_bytes)
        self.save_candle_to_json(stock_dict)

    def _price_url(self):
        if self.market == 'CN':
            return "https://query1.finance.yahoo.com/v7/finance/download/000001.SS?period1={}&period2={}&interval=1d&events=history&includeAdjustedClose=true".format(
                self.start_timestamp, self.end_timestamp)
        else:
            return "https://query1.finance.yahoo.com/v7/finance/download/%5EIXIC?period1={}&period2={}&interval=1d&events=history&includeAdjustedClose=true".format(
                self.start_timestamp, self.end_timestamp)

    def download_candle(self):
        url = self._price_url()
        try:
            index_bytes = requests.get(url).content

            if(self.IF_DEBUG):
                print("  download_candle()--> downloaded {} ".format(self.market))
            return index_bytes
        except:
            raise ValueError("ERROR: can not download {}".format(self.market))

    def convert_candle_data(self, index_bytes):
        """convert index_bytes to a dict, for json to save
        """
        date_list = []
        price_list = []
        vol_list = []
        try:
            index_bytes_split = index_bytes.split(b'\n')[1:]
            for d in index_bytes_split:
                day_data = str(d, 'utf-8').split(',')
                # print(day_data)
                date_list.append(day_data[0])

                if (day_data[5] != 'null'):
                    price_list.append(float(day_data[5]))
                else :
                    price_list.append(price_list[-1])
                    
                if (day_data[6] != 'null'):
                    vol_list.append(float(day_data[6]))
                else :
                    vol_list.append(vol_list[-1])
                assert len(date_list) == len(price_list), "ERROR: {} data did not inserted".format(day_data)
                
            assert len(date_list) == len(price_list), "ERROR: len(date_list) != len(price_list)"
            assert len(date_list) == len(vol_list), "ERROR: len(date_list) != len(vol_list)"
        except:
            raise ValueError("tiingo list has error!")
        split_list = [1 for i in date_list]
        
        if(self.IF_DEBUG):
            print("  convert_candle_data()--> for {} days, from {} to {}"
                  .format(len(date_list), date_list[0], date_list[-1]))
        stock_dict = {'date': date_list, 'c': price_list, 'v': vol_list, 'sp': split_list}

        stock_data_helper = StockDataHelper()
        ma_3, ma_13, ma_34 = stock_data_helper.ma_lists(price_list)
        assert len(date_list) == len(ma_3), "ERROR: len(date_list) != len(ma_3)"

        bull_list = stock_data_helper.bull_list(price_list)
        assert len(date_list) == len(bull_list), "ERROR: len(date_list) != len(bull_list)"

        stock_dict['3'] = ma_3
        stock_dict['13'] = ma_13
        stock_dict['34'] = ma_34
        stock_dict['BULL'] = bull_list
        return stock_dict

    def save_candle_to_json(self, stock_dict):
        try:
            JsonHelper().save_json("INDEX", stock_dict, self.market)
        except:
            raise ValueError("can not save json file {}_{}".format(self.market, "INDEX"))


if __name__ == "__main__":
    pass
