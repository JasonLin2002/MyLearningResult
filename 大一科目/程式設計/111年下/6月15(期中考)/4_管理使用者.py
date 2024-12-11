import tkinter as tk
from tkinter import messagebox
import mysql.connector
import hashlib

# 建立資料庫連線
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)

# 函式：開啟帳號管理視窗
def open_account_management():
    account_window = tk.Toplevel(main_window)
    account_window.title("帳號管理")
    account_window.geometry("300x300")
    
    # 函式：新增使用者
    def add_user():
        new_username = username_entry.get()
        new_password = password_entry.get()
        # 檢查使用者名稱是否已存在
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (new_username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            messagebox.showerror("錯誤", "使用者名稱已存在")
        else:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username, hashed_password))
            db.commit()
            messagebox.showinfo("成功", "使用者已新增")
        
    # 函式：查詢使用者
    def get_user():
        query_username = query_username_entry.get()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (query_username,))
        user = cursor.fetchone()
        
        if user:
            messagebox.showinfo("使用者資訊", f"使用者名稱: {user[1]}, 密碼: {user[2]}")
        else:
            messagebox.showerror("錯誤", "找不到該使用者")
    
    # 函式：修改使用者
    def update_user():
        update_username = update_username_entry.get()
        new_password = new_password_entry.get()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, update_username))
        db.commit()
        messagebox.showinfo("成功", "使用者已修改")
    
    # 函式：刪除使用者
    def delete_user():
        delete_username = delete_username_entry.get()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s", (delete_username,))
        db.commit()
        messagebox.showinfo("成功", "使用者已刪除")
    
    # 新增使用者區域
    add_label = tk.Label(account_window, text="新增使用者")
    add_label.pack()
    
    username_label = tk.Label(account_window, text="使用者名稱")
    username_label.pack()
    
    username_entry = tk.Entry(account_window)
    username_entry.pack()
    
    password_label = tk.Label(account_window, text="密碼")
    password_label.pack()
    
    password_entry = tk.Entry(account_window, show="*")
    password_entry.pack()
    
    add_button = tk.Button(account_window, text="新增", command=add_user)
    add_button.pack()
    
    # 查詢使用者區域
    query_label = tk.Label(account_window, text="查詢使用者")
    query_label.pack()
    
    query_username_label = tk.Label(account_window, text="使用者名稱")
    query_username_label.pack
