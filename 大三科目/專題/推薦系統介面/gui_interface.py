import tkinter as tk
from tkinter import ttk

def search_button_clicked():
    search_term1 = search_entry1.get()
    search_term2 = search_entry2.get()
    print(f"搜尋條件 1: {search_term1}")
    print(f"搜尋條件 2: {search_term2}")
    # 在這裡加入搜尋功能的程式碼

def search_button1_clicked():
    search_term1 = search_entry1.get()
    print(f"搜尋條件 1: {search_term1}")
    # 在這裡加入搜尋功能的程式碼

def search_button2_clicked():
    search_term2 = search_entry2.get()
    print(f"搜尋條件 2: {search_term2}")
    # 在這裡加入搜尋功能的程式碼

def resize_widgets(event):
    new_size = min(event.width // 50, event.height // 50)
    style.configure('TLabel', font=('Helvetica', new_size))
    style.configure('TButton', font=('Helvetica', new_size))
    style.configure('TEntry', font=('Helvetica', new_size))

# 建立主視窗
window = tk.Tk()
window.title("雄獅旅遊 推薦系統介面")
window.geometry('400x200')
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)

style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 12))
style.configure('TEntry', font=('Helvetica', 12))

window.bind('<Configure>', resize_widgets)

# 搜尋欄位 1
search_label1 = ttk.Label(window, text="搜尋欄位 1:", style='TLabel')
search_label1.grid(column=0, row=0, padx=5, pady=5, sticky='w')
search_entry1 = ttk.Entry(window, width=30, style='TEntry')
search_entry1.grid(column=1, row=0, padx=5, pady=5, sticky='ew')

# 搜尋按鈕 1
search_button1 = ttk.Button(window, text="搜尋", command=search_button1_clicked, style='TButton')
search_button1.grid(column=2, row=0, padx=5, pady=5, sticky='ew')

# 搜尋欄位 2
search_label2 = ttk.Label(window, text="搜尋欄位 2:", style='TLabel')
search_label2.grid(column=0, row=1, padx=5, pady=5, sticky='w')
search_entry2 = ttk.Entry(window, width=30, style='TEntry')
search_entry2.grid(column=1, row=1, padx=5, pady=5, sticky='ew')

# 搜尋按鈕 2
search_button2 = ttk.Button(window, text="搜尋", command=search_button2_clicked, style='TButton')
search_button2.grid(column=2, row=1, padx=5, pady=5, sticky='ew')

# 搜尋按鈕
#search_button = ttk.Button(window, text="搜尋", command=search_button_clicked)
#search_button.grid(column=1, row=2, padx=5, pady=10, sticky='e')

window.mainloop()
