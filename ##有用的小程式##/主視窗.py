import tkinter as tk
import 定時關機
import 消除特定名字
import 重新編號
import webp轉jpg

def open_window1():
    main_window.withdraw()
    win1.deiconify()

def open_window2():
    main_window.withdraw()
    win2.deiconify()

def open_window3():
    main_window.withdraw()
    win3.deiconify()

def open_window4():
    main_window.withdraw()
    win4.deiconify()

# 主視窗
main_window = tk.Tk()
main_window.title("主視窗")
main_window.geometry("500x400")

btn1 = tk.Button(main_window, text="打開定時關機", command=open_window1)
btn2 = tk.Button(main_window, text="打開消除特定名字", command=open_window2)
btn3 = tk.Button(main_window, text="打開重新編號", command=open_window3)
btn4 = tk.Button(main_window, text="webp轉jpg", command=open_window4)

# 創建子視窗
win1 = 定時關機.create_window(main_window)
win2 = 消除特定名字.create_window(main_window)
win3 = 重新編號.create_window(main_window)
win4 = webp轉jpg.create_window(main_window)

win1.withdraw()
win2.withdraw()
win3.withdraw()
win4.withdraw()

# 使用 grid 佈局按鈕
btn1.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
btn2.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")
btn3.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")
btn4.grid(row=3, column=0, padx=10, pady=10, sticky="NSEW")

# 設置行和列的權重，以使按鈕能夠自適應視窗大小
main_window.grid_rowconfigure(0, weight=1)
main_window.grid_rowconfigure(1, weight=1)
main_window.grid_rowconfigure(2, weight=1)
main_window.grid_rowconfigure(3, weight=1)
main_window.grid_columnconfigure(0, weight=1)

main_window.mainloop()
