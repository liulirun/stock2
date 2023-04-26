import json


class JsonHelper:
    """
    [summary]
    deals with data from api_hub
    """

    def __init__(self):
        self.debug = False
        self.json_path = './data/json'

    def read_json(self, stock_name):
        """
        read local json file, which has looks like 
        dict{'c': self.price_list, 'v': self.vol_list, 'date': self.date_list}
        """
        with open(f"{self.json_path}/{stock_name}.json") as json_file:
            json_data = json.load(json_file)
            if self.debug:
                print(f"  JsonHelper.read_json() --> read {self.json_path}/{stock_name}.json success")
        return json_data

    def save_json(self, stock_name, stock_dict, market):
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
        with open(f"{self.json_path}/{market}_{stock_name}.json", 'w') as f:
            json.dump(stock_dict, f)
            if self.debug:
                print(f"  JsonHelper.save_json() --> save {self.json_path}/{market}_{stock_name}.json success")


if __name__ == "__main__":
    pass
