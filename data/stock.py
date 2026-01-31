from data.api_hub import Apihub
from data.db_helper import DbHelper
from data.index_hub import Indexhub


# logic: download from apihub,handles json,save to MYSQL DB,and save json file
def run():
    """
    Entrance for data folder.
    Insert TICK data into Mysql.
    """
    apihub = Apihub()
    db_helper = DbHelper()

    market_lists = ['US','CN']
    for market in market_lists:
        indexhub = Indexhub(market=market)
        indexhub.run()
        db_helper.run("{}_{}".format(market,"INDEX"))

    US_lists = ['LABU','QQQ','SQ','TSLA','PDD','NIU',
                'UPST','BABA','YANG','YINN','COST',
                'GTLB','UBER','FNGU','SPY','TNA','IWM',
                'CRWD','ZS','VRT','NVDL','TSLL','SYM']
    for stock_name in US_lists:
        apihub.run(stock_name,market='US')
        db_helper.run("US_{}".format(stock_name))

    CN_dicts = {'002230': u'科大讯飞','300552': u'万集科技','300015': u'爱尔眼科',
                '600660': u'福耀玻璃','002038': u'双鹭药业','603288': u'海天味业'}
    for stock_name in CN_dicts.keys():
        apihub.run(stock_name,market='CN')
        db_helper.run("CN_{}".format(stock_name),CN_dicts[stock_name])


def clean_up_old_DB():
    # if table in DB 's last updates is 60 days ago,means we no longer watch this stock
    # then delete table
    pass


def test_run():
    pass


if __name__ == "__main__":
    run()
