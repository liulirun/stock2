from datetime import datetime


DEFAULT_DATE_START = "2010-01-01"
DEFAULT_DATE_END = datetime.now().date()
DEFAULT_MARKET = "US"

DEBUG_PRINT = "DEBUG_PRINT"
DEBUG_FAKE_API = "DEBUG_FAKE_API"
DEBUG_PRINT_TRUE = "PRINT"
DEBUG_PRINT_FALSE = "DO_NOT_PRINT"
DEBUG_FAKE_API_TRUE = "USE_FAKE_API"
DEBUG_FAKE_API_FALSE = "USE_REAL_API"

# US_STOCK_LISTS = ["TSLA"]
US_STOCK_LISTS = [
    # "CRWD",
    # "ZS",
    # "NVDL",
    # "TSLA",
    # "PDD",
    # "UPST",
    # "BABA",
    # "COST",
    # "UBER",
    # "QQQ",  # 纳指100ETF
    # "LABU",  # 三倍做多生物技术
    # "YANG",  # 三倍做空富时中国ETF-Direxion
    # "YINN",  # 三倍做多富时中国ETF-Direxion
    "TNA",  # 三倍做多小盘股ETF-Direxion
    "VRT",  # Vertiv Holdings
    "TSLL",  # 两倍做多特斯拉
]

# To be fixed
# "FNGU",  # 三倍做多FANG+指数ETN-MicroSector

#
# CN_STOCK_DICTS = {
#     "002230": "科大讯飞",
#     "300552": "万集科技",
#     "300015": "爱尔眼科",
#     "600660": "福耀玻璃",
#     "002038": "双鹭药业",
#     "603288": "海天味业",
