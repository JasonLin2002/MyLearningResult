import tkinter as tk
from tkinter import ttk

def search_button_clicked():
    search_term1 = search_entry1.get()
    search_term2 = search_entry2.get()
    print(f"搜尋條件 1: {search_term1}")
    print(f"搜尋條件 2: {search_term2}")
    # 在這裡加入搜尋功能的程式碼

# 建立主視窗
window = tk.Tk()
window.title("推薦系統介面")
window.geometry('400x200')

# 搜尋欄位 1
search_label1 = ttk.Label(window, text="搜尋欄位 1:")
search_label1.grid(column=0, row=0, padx=5, pady=5, sticky='w')
search_entry1 = ttk.Entry(window, width=30)
search_entry1.grid(column=1, row=0, padx=5, pady=5)

# 搜尋欄位 2
search_label2 = ttk.Label(window, text="搜尋欄位 2:")
search_label2.grid(column=0, row=1, padx=5, pady=5, sticky='w')
search_entry2 = ttk.Entry(window, width=30)
search_entry2.grid(column=1, row=1, padx=5, pady=5)

# 搜尋按鈕
search_button = ttk.Button(window, text="搜尋", command=search_button_clicked)
search_button.grid(column=1, row=2, padx=5, pady=10, sticky='e')

window.mainloop()
