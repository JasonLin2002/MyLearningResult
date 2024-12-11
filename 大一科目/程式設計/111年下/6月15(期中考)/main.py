import tkinter as tk

def validate_credentials():
    username = username_entry.get()
    password = password_entry.get()
    
    if username == "admin" and password == "password":
        run_program()
    else:
        error_label.config(text="錯誤的帳號或密碼")

def run_program():
    print("登入成功！執行程式中...")

window = tk.Tk()
window.title("帳號密碼驗證程式")

username_label = tk.Label(window, text="帳號：")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

password_label = tk.Label(window, text="密碼：")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

error_label = tk.Label(window, fg="red")
error_label.pack()

validate_button = tk.Button(window, text="驗證", command=validate_credentials)
validate_button.pack()

window.mainloop()
#--------------------------------------------------------------------以下主程式
