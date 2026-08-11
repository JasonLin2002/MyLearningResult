import tkinter as tk
import sys
import os

# 直接把四個工具當模組 import 進來（而不是用 subprocess 開新的 .py 檔）
# 這樣打包成 exe 後，所有功能都會被包進同一顆執行檔，不需要仰賴外部 .py 檔或系統上的 Python
import 定時關機
import 消除特定名字
import 重新編號
import webp轉jpg

def get_base_path():
    """獲取執行檔或腳本的基礎路徑"""
    if getattr(sys, 'frozen', False):
        # 如果是打包後的exe
        return sys._MEIPASS
    else:
        # 開發環境
        return os.path.dirname(os.path.abspath(__file__))

def open_window1():
    """開啟定時關機工具"""
    main_window.withdraw()
    定時關機.create_window(main_window)

def open_window2():
    """開啟消除特定名字工具"""
    main_window.withdraw()
    消除特定名字.create_window(main_window)

def open_window3():
    """開啟重新編號工具"""
    main_window.withdraw()
    重新編號.create_window(main_window)

def open_window4():
    """開啟webp轉jpg工具"""
    main_window.withdraw()
    webp轉jpg.create_window(main_window)

def on_closing():
    """關閉主視窗"""
    main_window.destroy()

# 創建主視窗
main_window = tk.Tk()
main_window.title("多功能工具箱")

# 設置視窗圖標
try:
    icon_path = os.path.join(get_base_path(), "阿農醬.ico")
    if os.path.exists(icon_path):
        main_window.iconbitmap(icon_path)
except Exception as e:
    print(f"載入圖標失敗：{e}")

main_window.geometry("500x400")
main_window.protocol("WM_DELETE_WINDOW", on_closing)

# 創建標題標籤
title_label = tk.Label(main_window, text="多功能工具箱", 
                       font=("Arial", 16, "bold"), fg="#2C3E50")
title_label.grid(row=0, column=0, pady=(20, 10))

# 創建按鈕
btn1 = tk.Button(main_window, text="定時關機", command=open_window1,
                 font=("Arial", 12), bg="#3498DB", fg="white", relief=tk.RAISED)
btn2 = tk.Button(main_window, text="消除特定名字", command=open_window2,
                 font=("Arial", 12), bg="#2ECC71", fg="white", relief=tk.RAISED)
btn3 = tk.Button(main_window, text="重新編號", command=open_window3,
                 font=("Arial", 12), bg="#E67E22", fg="white", relief=tk.RAISED)
btn4 = tk.Button(main_window, text="webp轉jpg", command=open_window4,
                 font=("Arial", 12), bg="#9B59B6", fg="white", relief=tk.RAISED)

# 使用 grid 佈局按鈕
btn1.grid(row=1, column=0, padx=50, pady=10, sticky="EW")
btn2.grid(row=2, column=0, padx=50, pady=10, sticky="EW")
btn3.grid(row=3, column=0, padx=50, pady=10, sticky="EW")
btn4.grid(row=4, column=0, padx=50, pady=10, sticky="EW")

# 設置行和列的權重，使按鈕能夠自適應視窗大小
main_window.grid_rowconfigure(0, weight=0)  # 標題列
main_window.grid_rowconfigure(1, weight=1)
main_window.grid_rowconfigure(2, weight=1)
main_window.grid_rowconfigure(3, weight=1)
main_window.grid_rowconfigure(4, weight=1)
main_window.grid_rowconfigure(5, weight=0)  # 底部留白
main_window.grid_columnconfigure(0, weight=1)

# 底部版權資訊
copyright_label = tk.Label(main_window, text="© 2026 多功能工具箱", 
                          font=("Arial", 9), fg="gray")
copyright_label.grid(row=5, column=0, pady=(10, 20))

# 啟動主循環
if __name__ == "__main__":
    main_window.mainloop()