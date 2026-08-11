import os
import tkinter as tk
from tkinter import filedialog, scrolledtext

def create_window(main_window):
    def choose_folder():
        folder_selected = filedialog.askdirectory()
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

    def apply_removal():
        folder_path = folder_entry.get()
        remove_word = remove_word_entry.get()
        if not folder_path or not remove_word:
            result_text.insert(tk.END, "請輸入資料夾路徑和要移除的字元\n")
            result_text.see(tk.END)
            return

        # 清空之前的訊息
        result_text.delete(1.0, tk.END)
        
        # 先收集所有需要重新命名的項目（目錄與檔案）
        items_to_rename = []

        try:
            # topdown=False 確保先走訪子目錄
            for root, dirs, files in os.walk(folder_path, topdown=False):
                # 處理目錄
                for dir_name in dirs:
                    if remove_word in dir_name:
                        old_path = os.path.join(root, dir_name)
                        new_name = dir_name.replace(remove_word, '')
                        new_path = os.path.join(root, new_name)
                        if old_path != new_path:
                            items_to_rename.append((old_path, new_path, True))
                
                # 處理檔案
                for file_name in files:
                    if remove_word in file_name:
                        old_path = os.path.join(root, file_name)
                        new_name = file_name.replace(remove_word, '')
                        new_path = os.path.join(root, new_name)
                        if old_path != new_path:
                            items_to_rename.append((old_path, new_path, False))

            # 依照深度排序：先處理檔案，再處理目錄（深層目錄優先）
            items_to_rename.sort(key=lambda x: (not x[2], -len(x[0]) if x[2] else 0))

            # 執行重新命名
            renamed_count = 0
            result_text.insert(tk.END, "開始處理...\n")
            result_text.see(tk.END)
            
            for old_path, new_path, is_dir in items_to_rename:
                try:
                    os.rename(old_path, new_path)
                    renamed_count += 1
                    if is_dir:
                        result_text.insert(tk.END, f"✓ 已重新命名目錄：{os.path.basename(old_path)} → {os.path.basename(new_path)}\n")
                    else:
                        result_text.insert(tk.END, f"✓ 已重新命名檔案：{os.path.basename(old_path)} → {os.path.basename(new_path)}\n")
                    # 更新視窗以顯示最新訊息
                    window.update()
                    result_text.see(tk.END)
                except Exception as e:
                    result_text.insert(tk.END, f"✗ 錯誤：{e}\n")
                    result_text.see(tk.END)
                    continue

            if renamed_count == 0:
                result_text.insert(tk.END, "沒有找到包含指定字詞的檔案或資料夾。\n")
            else:
                result_text.insert(tk.END, f"\n=== 處理完成！共重新命名 {renamed_count} 個項目。 ===\n")
            
            result_text.see(tk.END)

        except Exception as e:
            result_text.insert(tk.END, f"發生錯誤：{e}\n")
            result_text.see(tk.END)

    def back_to_main():
        window.withdraw()
        main_window.deiconify()

    window = tk.Toplevel(main_window)
    window.title("消除特定名字")
    window.geometry("800x600")  # 設定較大的視窗尺寸

    # 主框架
    main_frame = tk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # 輸入區域框架
    input_frame = tk.Frame(main_frame)
    input_frame.pack(fill=tk.X, pady=(0, 20))

    # 資料夾選擇區域
    folder_label = tk.Label(input_frame, text="輸入資料夾位址:", font=("Arial", 10))
    folder_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

    folder_entry = tk.Entry(input_frame, width=50, font=("Arial", 10))
    folder_entry.grid(row=1, column=0, sticky="ew", pady=(0, 5))

    button_choose = tk.Button(input_frame, text="選擇資料夾", command=choose_folder, font=("Arial", 10))
    button_choose.grid(row=1, column=1, padx=(10, 0), pady=(0, 5))

    # 移除字詞區域
    remove_word_label = tk.Label(input_frame, text="輸入要移除的字元:", font=("Arial", 10))
    remove_word_label.grid(row=2, column=0, sticky="w", pady=(10, 5))

    remove_word_entry = tk.Entry(input_frame, width=50, font=("Arial", 10))
    remove_word_entry.grid(row=3, column=0, sticky="ew", pady=(0, 5))

    button_apply = tk.Button(input_frame, text="套用", command=apply_removal, font=("Arial", 10), bg="#4CAF50", fg="white")
    button_apply.grid(row=3, column=1, padx=(10, 0), pady=(0, 5))

    # 設定grid的列權重
    input_frame.grid_columnconfigure(0, weight=1)

    # 結果顯示區域（使用滾動文字框）
    result_frame = tk.Frame(main_frame)
    result_frame.pack(fill=tk.BOTH, expand=True)

    result_label = tk.Label(result_frame, text="處理結果:", font=("Arial", 10, "bold"))
    result_label.pack(anchor="w", pady=(0, 5))

    result_text = scrolledtext.ScrolledText(result_frame, height=20, font=("Consolas", 9), wrap=tk.WORD)
    result_text.pack(fill=tk.BOTH, expand=True)

    # 底部按鈕區域
    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=(10, 0))

    back_btn = tk.Button(button_frame, text="返回主視窗", command=back_to_main, font=("Arial", 10), width=15)
    back_btn.pack(side=tk.RIGHT)

    return window

# 主視窗程式
if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("主視窗")
    main_window.geometry("300x200")
    
    # 建立一個按鈕來開啟子視窗
    btn_open = tk.Button(main_window, text="開啟消除工具", 
                        command=lambda: create_window(main_window),
                        font=("Arial", 12), width=15, height=2)
    btn_open.pack(pady=50)
    
    main_window.mainloop()