import tkinter as tk
from tkinter import messagebox
import mysql.connector
import hashlib

# 建立資料庫連線
db = mysql.connector.connect(
        host="localhost",
        user="jk121519",
        password="9843",
        database="final_report"
)

# 函式：帳密驗證
def login(account, password):
    # 將密碼使用 SHA256 雜湊演算法進行加密
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # 查詢資料庫中的使用者資訊
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE account = %s AND password = %s", (account, hashed_password))
    user = cursor.fetchone()
    
    if user:
        messagebox.showinfo("登入成功", "成功進入系統")
        open_account_management()
    else:
        messagebox.showerror("登入失敗", "帳號或密碼錯誤")

# 函式：開啟帳號管理視窗
def open_account_management():
    account_window = tk.Toplevel(main_window)
    account_window.title("帳號管理")
    account_window.geometry("300x300")
    
    # 函式：新增使用者
    def add_user():
        new_account = account_entry.get()
        new_password = password_entry.get()
        # 檢查使用者名稱是否已存在
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE account = %s", (new_account,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            messagebox.showerror("錯誤", "使用者名稱已存在")
        else:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            cursor.execute("INSERT INTO users (account, password) VALUES (%s, %s)", (new_account, hashed_password))
            db.commit()
            messagebox.showinfo("成功", "使用者已新增")
        
    # 函式：查詢使用者
    def get_user():
        query_account = query_account_entry.get()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE account = %s", (query_account,))
        user = cursor.fetchone()
        
        if user:
            messagebox.showinfo("使用者資訊", f"使用者名稱: {user[1]}, 密碼: {user[2]}")
        else:
            messagebox.showerror("錯誤", "找不到該使用者")
    
    # 函式：修改使用者
    def update_user():
        update_account = update_account_entry.get()
        new_password = new_password_entry.get()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE account = %s", (new_password, update_account))
        db.commit()
        messagebox.showinfo("成功", "使用者已修改")
    
    # 函式：刪除使用者
    def delete_user():
        delete_account = delete_account_entry.get()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE account = %s", (delete_account,))
        db.commit()
        messagebox.showinfo("成功", "使用者已刪除")
    
    # 新增使用者區域
    add_label = tk.Label(account_window, text="新增使用者")
    add_label.pack()
    
    account_label = tk.Label(account_window, text="使用者名稱")
    account_label.pack()
    
    account_entry = tk.Entry(account_window)
    account_entry.pack()
    
    password_label = tk.Label(account_window, text="密碼")
    password_label.pack()
    
    password_entry = tk.Entry(account_window, show="*")
    password_entry.pack()
    
    add_button = tk.Button(account_window, text="新增", command=add_user)
    add_button.pack()
    
    # 查詢使用者區域
    query_label = tk.Label(account_window, text="查詢使用者")
    query_label.pack()
    
    query_account_label = tk.Label(account_window, text="使用者名稱")
    query_account_label.pack()
    
    query_account_entry = tk.Entry(account_window)
    query_account_entry.pack()
    
    query_button = tk.Button(account_window, text="查詢", command=get_user)
    query_button.pack()
    
    # 修改使用者區域
    update_label = tk.Label(account_window, text="修改使用者")
    update_label.pack()
    
    update_account_label = tk.Label(account_window, text="使用者名稱")
    update_account_label.pack()
    
    update_account_entry = tk.Entry(account_window)
    update_account_entry.pack()
    
    new_password_label = tk.Label(account_window, text="新密碼")
    new_password_label.pack()
    
    new_password_entry = tk.Entry(account_window, show="*")
    new_password_entry.pack()
    
    update_button = tk.Button(account_window, text="修改", command=update_user)
    update_button.pack()
    
    # 刪除使用者區域
    delete_label = tk.Label(account_window, text="刪除使用者")
    delete_label.pack()
    
    delete_account_label = tk.Label(account_window, text="使用者名稱")
    delete_account_label.pack()
    
    delete_account_entry = tk.Entry(account_window)
    delete_account_entry.pack()
    
    delete_button = tk.Button(account_window, text="刪除", command=delete_user)
    delete_button.pack()

# 主視窗
main_window = tk.Tk()
main_window.title("登入系統")
main_window.geometry("300x200")

account_label = tk.Label(main_window, text="帳號")
account_label.pack()

account_entry = tk.Entry(main_window)
account_entry.pack()

password_label = tk.Label(main_window, text="密碼")
password_label.pack()

password_entry = tk.Entry(main_window, show="*")
password_entry.pack()

login_button = tk.Button(main_window, text="登入", command=lambda: login(account_entry.get(), password_entry.get()))
login_button.pack()

main_window.mainloop()

# 關閉資料庫連線
db.close()
