from analyze.algo_daily import Algo_Daily
from data import stock
from mysql.backup import Backup

if __name__ == "__main__":
    print("1. insert to mysql DB")
    stock.run()

    print("2. push mysql DB to docker hub")
    Backup().run()

    print("3. generate daily png")
    c = Algo_Daily()
    c.run(market='US')
    c.run(market='CN')
