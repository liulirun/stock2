import json
import os
from data.const import *


class JsonHelper:
    """
    [summary]
    deals with data from fetch_stock_data_from_api
    """

    def __init__(self):
        self.debug_print = os.environ.get(DEBUG_PRINT)
        self.debug_save_to_json = os.environ.get(DEBUG_FAKE_API)
        self.json_path = "./data/json"

    def read_json(self, stock_name):
        """
        read local json file, which has looks like
        dict{'c': self.price_list, 'v': self.vol_list, 'date': self.date_list}
        """
        with open(f"{self.json_path}/{stock_name}.json") as json_file:
            json_data = json.load(json_file)
            if self.debug_print == DEBUG_PRINT_TRUE:
                print(
                    f"  JsonHelper.read_json() --> read {self.json_path}/{stock_name}.json success"
                )
        return json_data

    def save_json(self, market, file_name, stock_dict):
        """
        save price list to local json file
        stock_dict = {'date': date_list,
                     'c': price_list,
                     'v': vol_list,
                     '3': ma_3,
                     '13': ma_13,
                     '34': ma_34,
                     'BULL':bull_list,
                     'sp':split_list
                     }
        """
        if self.debug_save_to_json == DEBUG_FAKE_API_TRUE:
            print("debug, won't save to json")
            return
        try:
            with open(
                file=f"{self.json_path}/{market}_{file_name}.json", mode="w"
            ) as f:
                json.dump(obj=stock_dict, fp=f)
                if self.debug_print == DEBUG_PRINT_TRUE:
                    print(
                        f"  JsonHelper.save_json() --> save {self.json_path}/{market}_{file_name}.json success"
                    )
        except:
            raise ValueError("can not save json file {}_{}".format(market, file_name))


if __name__ == "__main__":
    pass
