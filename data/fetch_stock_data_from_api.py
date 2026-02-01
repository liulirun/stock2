import os
import requests
from credential import cred
from data.json_helper import JsonHelper
from data.stock_data_helper import StockDataHelper
from data.const import *


class ApiFetch:
    def __init__(self):
        self.token = cred.tiingo["token"]
        self.root_url = cred.tiingo["root_url"]
        self.debug_print = os.environ.get(DEBUG_PRINT)
        self.debug_fake_api_result = os.environ.get(DEBUG_FAKE_API)

    def fetch_and_save_to_json(
        self,
        stock_name,
        date_start=DEFAULT_DATE_START,
        date_end=DEFAULT_DATE_END,
        market=DEFAULT_MARKET,
        if_index=False,
    ):
        # use SPY for US market index, as tiingo does not have other index stock
        json_file_name = stock_name
        if if_index:
            stock_name = "SPY"
            json_file_name = "INDEX"
        if self.debug_print == DEBUG_PRINT_TRUE:
            print("fetch_and_save_to_json().run() --> for stock {}".format(stock_name))

        tiingo_list = self.fetch_from_api(
            stock_name=stock_name, date_start=date_start, date_end=date_end
        )
        stock_dict = self.convert_candle_data(tiingo_list=tiingo_list)
        JsonHelper().save_json(
            market=market, file_name=json_file_name, stock_dict=stock_dict
        )

    def fetch_from_api(self, stock_name, date_start, date_end):
        """
        Download stock Candles data from tiingo, in list format.
        tiingo will return a dict {'detail':'failed reason'} if download failed.
        """
        tiingo_list = []
        url = self._price_url(
            stock_name=stock_name, date_start=date_start, date_end=date_end
        )
        try:
            if self.debug_fake_api_result == DEBUG_FAKE_API_TRUE:
                return self.fake_tiingo_list()

            headers = {"Content-Type": "application/json"}
            tiingo_list = requests.get(url=url, headers=headers).json()

            assert isinstance(
                tiingo_list, list
            ), "ERROR: tiingo_list type is not a list"
            if self.debug_print == DEBUG_PRINT_TRUE:
                print("  fetch_from_api()--> downloaded {} ".format(stock_name))
            return tiingo_list
        except:
            raise ValueError(
                "ERROR: can not download {} from tiingo".format(stock_name)
            )

    def convert_candle_data(self, tiingo_list):
        """convert tiingo_list to a dict, for json to save"""
        try:
            assert len(tiingo_list) > 0, "tiingo_list is empty"
            date_list_pre = [d["date"] for d in tiingo_list]
            date_list = [
                str(datetime.strptime(i, "%Y-%m-%dT%H:%M:%S.%f%z").date())
                for i in date_list_pre
            ]
            price_list = [d["adjClose"] for d in tiingo_list]
            vol_list = [d["adjVolume"] for d in tiingo_list]
            split_list = [d["splitFactor"] for d in tiingo_list]
            assert len(date_list) == len(
                price_list
            ), "ERROR: len(date_list) != len(price_list)"
            assert len(date_list) == len(
                vol_list
            ), "ERROR: len(date_list) != len(vol_list)"
        except:
            raise ValueError("tiingo list has error!")

        if self.debug_print == DEBUG_PRINT_TRUE:
            print(
                "  convert_candle_data()--> for {} days, from {} to {}".format(
                    len(date_list), date_list[0], date_list[-1]
                )
            )
        stock_dict = {
            "date": date_list,
            "c": price_list,
            "v": vol_list,
            "sp": split_list,
        }

        stock_data_helper = StockDataHelper()
        ma_3, ma_13, ma_34 = stock_data_helper.ma_lists(price_list)
        assert len(date_list) == len(ma_3), "ERROR: len(date_list) != len(ma_3)"

        bull_list = stock_data_helper.bull_list(price_list)
        assert len(date_list) == len(
            bull_list
        ), "ERROR: len(date_list) != len(bull_list)"

        stock_dict["3"] = ma_3
        stock_dict["13"] = ma_13
        stock_dict["34"] = ma_34
        stock_dict["BULL"] = bull_list
        return stock_dict

    # def save_candle_to_json(
    #     self,
    #     market,
    #     file_name,
    #     stock_dict,
    # ):
    #     try:
    #         JsonHelper().save_json(
    #             market=market, file_name=file_name, stock_dict=stock_dict
    #         )
    #     except:
    #         raise ValueError("can not save json file {}_{}".format(market, file_name))

    def _price_url(self, stock_name, date_start, date_end):
        return "{}/{}/prices?startDate={}&endDate={}&token={}".format(
            self.root_url, stock_name, date_start, date_end, self.token
        )

    def fake_tiingo_list(self):
        return [
            {
                "date": "2026-01-29T00:00:00.000Z",
                "close": 694.04,
                "high": 697.06,
                "low": 684.83,
                "open": 696.39,
                "volume": 97486198,
                "adjClose": 694.04,
                "adjHigh": 697.06,
                "adjLow": 684.83,
                "adjOpen": 696.39,
                "adjVolume": 97486198,
                "divCash": 0.0,
                "splitFactor": 1.0,
            },
            {
                "date": "2026-01-30T00:00:00.000Z",
                "close": 691.97,
                "high": 694.21,
                "low": 687.12,
                "open": 691.79,
                "volume": 101835131,
                "adjClose": 691.97,
                "adjHigh": 694.21,
                "adjLow": 687.12,
                "adjOpen": 691.79,
                "adjVolume": 101835131,
                "divCash": 0.0,
                "splitFactor": 1.0,
            },
        ]
