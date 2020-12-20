from data.api_hub import Apihub
from data.db_helper import DbHelper


# logic: download from apihub, handles json, save to MYSQL DB, and save json file
def run():
    """
    Entrance for data folder.
    Insert TICK data into Mysql.
    """
    apihub = Apihub()
    db_helper = DbHelper()

    US_lists = ['QQQ', 'CRSP', 'TTD', 'SQ', 'BIGC', 'TSLA', 'PDD', 'TDOC', 'OKTA', 'ZUO', 'OOMA']
    for stock_name in US_lists:
        apihub.run(stock_name, market='US')
        db_helper.run("US_{}".format(stock_name))
        print("\n=======================\n")

    CN_lists = ['002230', '300552', '000001', '300015', '600660', '002038', '603288']
    for stock_name in CN_lists:
        apihub.run(stock_name, market='CN')
        db_helper.run("CN_{}".format(stock_name))
        print("\n=======================\n")


def clean_up_old_DB():
    # if table in DB 's last updates is 60 days ago, means we no longer watch this stock
    # then delete table
    pass


def test_run():
    pass


if __name__ == "__main__":
    run()
