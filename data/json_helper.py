import json


class JsonHelper:
    """
    [summary]
    deals with data from api_hub
    """

    def __init__(self):
        self.IF_DEBUG = True

    def read_json(self, stock_name):
        """
        read local json file, which has looks like 
        dict{'c': self.price_list, 'v': self.vol_list, 'date': self.date_list}
        """
        with open("./data/{}.json".format(stock_name)) as json_file:
            json_data = json.load(json_file)
            if self.IF_DEBUG:
                print("  JsonHelper.read_json() --> read ./data/{}.json success".format(stock_name))
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
                     'BULL':bull_list
                     }
        """
        with open("./data/{}_{}.json".format(market, stock_name), 'w') as f:
            json.dump(stock_dict, f)
            if self.IF_DEBUG:
                print("  JsonHelper.save_json() --> save ./data/{}_{}.json success".format(market, stock_name))


if __name__ == "__main__":
    pass
