from data import stock
from mysql.backup import Backup

if __name__ == "__main__":
    print("insert to mysql DB")
    stock.run()

    print("push mysql DB to docker hub")
    b = Backup()
    b.backup_mysql()
    b.push_mysql_image()
