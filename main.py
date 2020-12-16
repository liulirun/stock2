from data import run
from mysql import backup

if __name__ == "__main__":
    print("insert to mysql DB")
    run.run()

    print("push mysql DB to docker hub")
    b = backup.Backup()
    b.backup_mysql()
    b.push_mysql_image()
