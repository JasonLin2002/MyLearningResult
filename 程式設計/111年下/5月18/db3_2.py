import mysql.connector as myconn
import hashlib

dbConn = myconn.connect(
    host = "localhost",
    user = "jk121519",
    password = "0980043",
    database = "testdb2"
)

my_cursor = dbConn.cursor()
sql = "SELECT * FROM `users` WHERE account LIKE 'ja%';"
my_cursor.execute(sql)
result = my_cursor.fetchall()
for row in result:
    print(row)
sq13 = "DELETE FROM `users` WHERE id = 5;"
my_cursor.execute(sql3)
dbConn.commit()
print()
sql = "SELECT * FROM `users` ORDER BY id ASC"
