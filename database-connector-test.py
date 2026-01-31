import mysql.connector
from credential import cred

cnx = mysql.connector.connect(
    host=cred.mysqlDB["url"],
    user=cred.mysqlDB["user"],
    port=3306,
    password=cred.mysqlDB["password"],
)
cur = cnx.cursor()

query_curdate = "SELECT CURDATE()"
cur.execute(query_curdate)
row = cur.fetchone()
print("Current date is: {0}".format(row[0]))

query_table = "DESCRIBE stock.CN_002038"
cur.execute(query_table)
row = cur.fetchall()
print(f"Table: {row}")

query_from_DB = "SELECT * FROM stock.CN_002038 LIMIT 10;"
cur.execute(query_from_DB)
row = cur.fetchone()
print("First Row is: {0}".format(row[0]))

# Close connection
cnx.close()
