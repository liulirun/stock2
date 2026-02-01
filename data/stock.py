import os
from data.fetch_stock_data_from_api import ApiFetch
from data.db_helper import DbHelper
from data.const import *


def run():
    """
    Entrance for data folder, Insert TICK data into Mysql.
    logic:
        -. download index ( US uses SPY, China TBD) -- this is used for later determine a market is bull or bear
        -. download stock
        -. create json,
        -. save to MYSQL DB,
        -. and save json file
    """
    set_debug_option()
    apiFetch = ApiFetch()
    db_helper = DbHelper()

    # apiFetch.fetch_and_save_to_json(stock_name="", if_index=True)
    # db_helper.save_stock_to_database(table_name="US_{}".format("INDEX"))

    for stock_name in US_STOCK_LISTS:
        apiFetch.fetch_and_save_to_json(stock_name=stock_name)
        db_helper.save_stock_to_database(table_name="US_{}".format(stock_name))

    # disable CN for now, #TODO
    # for stock_name in CN_STOCK_DICTS.keys():
    #     apiFetch.fetch_and_save_to_json(stock_name, market="CN")
    #     db_helper.save_stock_to_database("CN_{}".format(stock_name), CN_dicts[stock_name])


def set_debug_option():
    os.environ[DEBUG_PRINT] = DEBUG_PRINT_TRUE
    os.environ[DEBUG_FAKE_API] = DEBUG_FAKE_API_FALSE


def clean_up_old_DB():
    # if table in DB 's last updates is 60 days ago,means we no longer watch this stock
    # then delete table
    pass


def test_run():
    pass


if __name__ == "__main__":
    run()
