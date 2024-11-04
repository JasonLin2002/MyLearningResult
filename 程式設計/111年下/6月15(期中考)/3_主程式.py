from tkinter import *
import mysql.connector

def add_user():
    mydb = mysql.connector.connect(
      host="localhost",
      user="yourusername",
      password="yourpassword",
      database="mydatabase"
    )

    mycursor = mydb.cursor()

    username = new_username_entry.get()
    password = new_password_entry.get()

    sql = "INSERT INTO users (username, password) VALUES (%s, SHA2(%s, 256))"
    val = (username, password)

    mycursor.execute(sql, val)

    mydb.commit()

def search_user():
    mydb = mysql.connector.connect(
      host="localhost",
      user="yourusername",
      password="yourpassword",
      database="mydatabase"
    )

    mycursor = mydb.cursor()

    username = search_username_entry.get()

    sql = "SELECT * FROM users WHERE username LIKE %s"
    val = ("%" + username + "%", )

    mycursor.execute(sql, val)

    results_listbox.delete(0, END)

    for result in mycursor:
        results_listbox.insert(END, result[1])

def update_user():
    mydb = mysql.connector.connect(
      host="localhost",
      user="yourusername",
      password="yourpassword",
      database="mydatabase"
    )

    mycursor = mydb.cursor()

    old_username = old_username_entry.get()
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()

    sql = "UPDATE users SET username=%s, password=SHA2(%s, 256) WHERE username=%s"
    val = (new_username, new_password, old_username)

    mycursor.execute(sql, val)

    mydb.commit()

def delete_user():
    mydb = mysql.connector.connect(
      host="localhost",
      user="yourusername",
      password="yourpassword",
      database="mydatabase"
    )

    mycursor = mydb.cursor()

    username_to_delete = delete_username_entry.get()

    sql = "DELETE FROM users WHERE username=%s"
    val = (username_to_delete, )

    mycursor.execute(sql, val)

    mydb.commit()

root = Tk()
root.title("User Management")

add_user_frame = Frame(root)
add_user_frame.pack(side=LEFT)

add_user_label = Label(add_user_frame, text="Add User")
add_user_label.pack()

new_username_label = Label(add_user_frame, text="Username")
new_username_label.pack()

new_username_entry = Entry(add_user_frame)
new_username_entry.pack