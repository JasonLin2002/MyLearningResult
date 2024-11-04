import tkinter as tk
from tkinter import ttk
import os

def create_window(main_window):
    def schedule_shutdown():
        hours = int(hours_entry.get() if hours_entry.get().isdigit() else 0)
        minutes = int(minutes_entry.get() if minutes_entry.get().isdigit() else 0)
        seconds = int(seconds_entry.get() if seconds_entry.get().isdigit() else 0)
        total_seconds = hours * 3600 + minutes * 60 + seconds
        
        if total_seconds > 0:
            os.system(f"shutdown -s -t {total_seconds}")
        else:
            print("請輸入有效的時間！")

    def back_to_main():
        window.withdraw()
        main_window.deiconify()

    window = tk.Toplevel(main_window)
    window.title("Windows 定時關機")

    tk.Label(window, text="小時:").grid(row=0, column=0)
    hours_entry = tk.Entry(window)
    hours_entry.grid(row=0, column=1)

    tk.Label(window, text="分鐘:").grid(row=1, column=0)
    minutes_entry = tk.Entry(window)
    minutes_entry.grid(row=1, column=1)

    tk.Label(window, text="秒數:").grid(row=2, column=0)
    seconds_entry = tk.Entry(window)
    seconds_entry.grid(row=2, column=1)

    execute_button = ttk.Button(window, text="執行", command=schedule_shutdown)
    execute_button.grid(row=3, column=0, columnspan=2)

    back_btn = tk.Button(window, text="返回主視窗", command=back_to_main)
    back_btn.grid(row=4, column=0, columnspan=2)

    return window
