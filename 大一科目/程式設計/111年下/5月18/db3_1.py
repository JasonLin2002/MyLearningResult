import mysql.connector as myconn
import hashlib

dbConn = myconn.connect(
    host = "localhost",
    user = "jk121519",
    password = "0980043",
    database = "testdb2"
)

my_cursor = dbConn.cursor()
sql = "SELECT * FROM `users` LIMIT 3;"
my_cursor.execute(sql)
result = my_cursor.fetchall()
for row in result:
    print(row)