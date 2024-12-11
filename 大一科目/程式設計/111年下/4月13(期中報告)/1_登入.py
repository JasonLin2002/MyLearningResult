import tkinter as tk
from tkinter import messagebox

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        self.label_username = tk.Label(root, text="Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(root)
        self.entry_username.pack()
        
        self.label_password = tk.Label(root, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()
        
        self.button_login = tk.Button(root, text="Login", command=self.login)
        self.button_login.pack()
        
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if username == "admin" and password == "admin":
            self.root.destroy()
            import os
            os.system('2_主要功能.py')

        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()