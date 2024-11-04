from tkinter import *
import mysql.connector
import subprocess


def login():
    mydb = mysql.connector.connect(
      host="localhost",
      user="jk121519",
      password="9843",
      database="final_report"
    )

    mycursor = mydb.cursor()

    account = account_entry.get()
    password = password_entry.get()

    sql = "SELECT * FROM users WHERE account = %s AND password = SHA2(%s, 256)"
    val = (account, password)

    mycursor.execute(sql, val)

    result = mycursor.fetchone()

    if result:
        print("Login successful!")
        open_main_window()  # 登入成功後開啟主視窗
    else:
        print("Invalid account or password.")

def open_main_window():
    subprocess.call(['python', '4_管理使用者.py'])
    # 在此處撰寫開啟主視窗的程式碼
    # 可以使用Tkinter或其他任何適合的庫來創建和顯示主視窗

root = Tk()
root.title("Login")

account_label = Label(root, text="account")
account_label.pack()

account_entry = Entry(root)
account_entry.pack()

password_label = Label(root, text="Password")
password_label.pack()

password_entry = Entry(root, show="*")
password_entry.pack()

login_button = Button(root, text="Login", command=login)
login_button.pack()

root.mainloop()