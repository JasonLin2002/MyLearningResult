import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def natural_sort_key(s):
    """
    自然排序的關鍵函數，將字串中的數字部分轉為整數進行比較
    例如：'file10.txt' 會排在 'file2.txt' 後面
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def create_window(main_window):
    def choose_folder():
        folder_selected = filedialog.askdirectory()
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

    def apply_rename():
        folder_path = folder_entry.get()
        if not folder_path:
            messagebox.showerror("錯誤", "請選擇資料夾")
            return
        
        try:
            start_index = int(start_index_entry.get())
            if start_index < 0:
                messagebox.showerror("錯誤", "起始編號必須大於等於 0")
                return
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字")
            return
        
        rename_files_in_folder(folder_path, start_index)

    def rename_files_in_folder(folder_path, start_index):
        try:
            # 取得所有檔案
            files = os.listdir(folder_path)
            
            # 過濾掉資料夾，只處理檔案
            files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
            
            if not files:
                messagebox.showinfo("提示", "資料夾中沒有檔案")
                return
            
            # 使用自然排序
            files.sort(key=natural_sort_key)
            
            # 顯示排序後的檔案順序（供確認）
            print("排序後的檔案順序：")
            for i, file_name in enumerate(files):
                print(f"{i+1}. {file_name}")
            
            # 重新命名
            renamed_count = 0
            for i, file_name in enumerate(files, start=start_index):
                _, file_extension = os.path.splitext(file_name)
                new_name = f"{i:03d}{file_extension}"
                old_path = os.path.join(folder_path, file_name)
                new_path = os.path.join(folder_path, new_name)
                
                # 如果新名稱已經存在，跳過或處理衝突
                if os.path.exists(new_path) and old_path != new_path:
                    # 可以選擇加上時間戳或編號避免衝突
                    base_name = f"{i:03d}"
                    counter = 1
                    while os.path.exists(os.path.join(folder_path, f"{base_name}_{counter:02d}{file_extension}")):
                        counter += 1
                    new_name = f"{base_name}_{counter:02d}{file_extension}"
                    new_path = os.path.join(folder_path, new_name)
                
                try:
                    os.rename(old_path, new_path)
                    renamed_count += 1
                    print(f"已重新命名：{file_name} → {new_name}")
                except Exception as e:
                    print(f"重新命名失敗：{file_name} - {e}")
            
            messagebox.showinfo("完成", f"成功重新命名 {renamed_count} 個檔案！")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"處理過程中發生錯誤：{e}")

    def back_to_main():
        window.withdraw()
        main_window.deiconify()

    window = tk.Toplevel(main_window)
    window.title("重新編號")
    window.geometry("400x400")

    # 主框架 - 使用 pack 並置中
    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    # 標題
    title_label = tk.Label(main_frame, text="重新編號工具", font=("Arial", 14, "bold"))
    title_label.pack(pady=(0, 20))

    # 資料夾選擇區域
    folder_label = tk.Label(main_frame, text="輸入資料夾位址:", font=("Arial", 10))
    folder_label.pack(anchor="w", pady=(0, 5))

    folder_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
    folder_entry.pack(pady=(0, 10))

    button_choose = tk.Button(main_frame, text="選擇資料夾", command=choose_folder, 
                             font=("Arial", 10), width=15)
    button_choose.pack(pady=(0, 15))

    # 起始編號區域
    start_label = tk.Label(main_frame, text="起始編號:", font=("Arial", 10))
    start_label.pack(anchor="w", pady=(0, 5))

    start_index_entry = tk.Entry(main_frame, width=10, font=("Arial", 10))
    start_index_entry.pack(pady=(0, 15))
    start_index_entry.insert(0, "1")

    # 說明文字
    info_label = tk.Label(main_frame, text="※ 會自動按照檔案名稱的數字順序排序", 
                          font=("Arial", 9), fg="gray")
    info_label.pack(pady=(0, 20))

    # 按鈕區域 - 使用 pack 並置中
    button_frame = tk.Frame(main_frame)
    button_frame.pack()

    button_apply = tk.Button(button_frame, text="套用", command=apply_rename,
                            font=("Arial", 10), bg="#4CAF50", fg="white", width=12)
    button_apply.pack(side=tk.LEFT, padx=(0, 10))

    back_btn = tk.Button(button_frame, text="返回主視窗", command=back_to_main,
                        font=("Arial", 10), width=12)
    back_btn.pack(side=tk.LEFT)

    return window

# 主視窗程式
if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("主視窗")
    main_window.geometry("300x200")
    
    btn_open = tk.Button(main_window, text="開啟重新編號工具", 
                        command=lambda: create_window(main_window),
                        font=("Arial", 12), width=15, height=2)
    btn_open.pack(expand=True)
    
    main_window.mainloop()