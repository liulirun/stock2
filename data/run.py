from data.api_hub import Apihub
from data.db_helper import DbHelper


# logic: download from apihub, handles json, save to MYSQL DB, and save json file
def run():
    """
    loop generate or insert TICK into Myql
    """

    apihub = Apihub()
    db_helper = DbHelper()
    stock_list = ['CRSP', 'TTD', 'SQ', 'BIGC', 'TSLA', 'PDD', 'TDOC']
    for stock_name in stock_list:
        apihub.run(stock_name, market='US')
        db_helper.run("US_{}".format(stock_name))
        print("\n=======================\n")


def clean_up_old_DB():
    # if table in DB 's last updates is 60 days ago, means we no longer watch this stock
    # then delete table
    pass


def test_run():
    pass


if __name__ == "__main__":
    test_run()
