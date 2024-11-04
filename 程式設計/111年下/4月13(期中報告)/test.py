import os
import tkinter as tk
from 登入 import Login


def start_main_program():
    os.system('Main.py')


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    login_window = Login(master=root)

    # 開啟登入介面
    login_window.mainloop()