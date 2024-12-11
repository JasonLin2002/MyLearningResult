import mysql.connector
import hashlib

mydb = mysql.connector.connect(
  host="localhost",
  user="jk121519",
  password="9843",
  database="final_report"
)

mycursor = mydb.cursor()

mycursor.execute("""
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        account VARCHAR(255),
        name VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255)
    )
""")

sql = 'INSERT INTO `users` (account, name, email, password) VALUES (%s, %s, %s, %s)'

m = hashlib.sha256()
pws = ['abcd1234', 'password1', 'security']
pws_h = []
for pw in pws:
    m.update(pw.encode('utf-8'))
    pws_h.append(m.hexdigest())

records = [('hsien', 'Hsien Lin', 'hsien@fcu.edu.tw', pws_h[0]),
          ('Jason', 'Jason Wu', 'jason@fcu.edu.tw', pws_h[1]),
          ('Allen', 'Allen Wang', 'allen@fcu.edu.tw', pws_h[2])]

mycursor.executemany(sql, records)
mydb.commit()