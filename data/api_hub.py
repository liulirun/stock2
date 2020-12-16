import json
from datetime import date, datetime

import requests
from credential import cred
from data.json_helper import JsonHelper
from data.stock_data_helper import StockDataHelper


class Apihub:
    def __init__(self):
        self.IF_DEBUG = True
        self.token = cred.tiingo["token"]
        self.root_url = cred.tiingo["root_url"]

    def run(self, stock_name, date_start='2010-01-01', date_end=datetime.now().date(), market='US'):
        if (self.IF_DEBUG):
            print("start Apihub.run() for stock {}".format(stock_name))
        tiingo_list = self.download_candle(stock_name, date_start, date_end)
        stock_dict = self.convert_candle_data(tiingo_list)
        self.save_candle_to_json(stock_name, stock_dict, market)
            
    def _price_url(self, stock_name, date_start, date_end):
        return "{}/{}/prices?startDate={}&endDate={}&token={}".format(self.root_url, stock_name, date_start, date_end, self.token)

    def download_candle(self, stock_name, date_start, date_end):
        """
        Download stock Candles data from tiingo, in list format. 
        tiingo will return a dict {'detail':'failed reason'} if download failed. 
        """
        headers = {'Content-Type': 'application/json'}
        url = self._price_url(stock_name, date_start, date_end)
        try:
            tiingo_list = requests.get(url, headers=headers).json()
            assert isinstance(tiingo_list, list), "ERROR: tiingo_list type is not a list"
            if(self.IF_DEBUG):
                print("  download_candle()--> downloaded {} ".format(stock_name))
            return tiingo_list
        except:
            raise ValueError("ERROR: can not download {} from tiingo".format(stock_name))

    def convert_candle_data(self, tiingo_list):
        """convert tiingo_list to a dict, for json to save
        """
        try:
            assert len(tiingo_list) > 0, "tiingo_list is empty"
            date_list_pre=[d['date'] for d in tiingo_list]
            date_list=[str(datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.%f%z').date()) for i in date_list_pre]
            price_list=[d['adjClose'] for d in tiingo_list]
            vol_list=[d['adjVolume'] for d in tiingo_list]
            assert len(date_list) == len(price_list), "ERROR: len(date_list) != len(price_list)"
            assert len(date_list) == len(vol_list), "ERROR: len(date_list) != len(vol_list)"
        except:
            raise ValueError("tiingo list has error!")

        if(self.IF_DEBUG):
            print("  convert_candle_data()--> for {} days, from {} to {}"
                  .format(len(date_list), date_list[0], date_list[-1]))
        stock_dict={'date': date_list, 'c': price_list, 'v': vol_list}

        stock_data_helper=StockDataHelper()
        ma_3, ma_13, ma_34=stock_data_helper.ma_lists(price_list)
        assert len(date_list) == len(ma_3), "ERROR: len(date_list) != len(ma_3)"

        bull_list=stock_data_helper.bull_list(price_list)
        assert len(date_list) == len(bull_list), "ERROR: len(date_list) != len(bull_list)"

        stock_dict['3']=ma_3
        stock_dict['13']=ma_13
        stock_dict['34']=ma_34
        stock_dict['BULL']=bull_list
        return stock_dict

    def save_candle_to_json(self, stock_name, stock_dict, market):
        try:
            JsonHelper().save_json(stock_name, stock_dict, market)
        except:
            raise ValueError("can not save json file {}_{}".format(market, stock_name))


if __name__ == "__main__":
    # h=Apihub()
    # h.run('TSLA', date_start='2020-01-01', date_end='2020-10-01')
    pass
