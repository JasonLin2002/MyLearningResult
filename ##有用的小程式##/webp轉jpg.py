import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image
import threading

def convert_webp_to_jpg(directory, result_text):
    """遍歷指定資料夾及其子資料夾，將所有 .webp 檔案轉換為 .jpg"""
    count = 0
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(".webp"):
                webp_path = os.path.join(foldername, filename)
                jpg_path = os.path.join(foldername, os.path.splitext(filename)[0] + ".jpg")
                
                try:
                    with Image.open(webp_path) as img:
                        img = img.convert("RGB")
                        img.save(jpg_path, "JPEG")
                    os.remove(webp_path)  # 刪除原始 WebP 檔案
                    result_text.insert(tk.END, f"轉換成功: {webp_path} -> {jpg_path}\n")
                    result_text.see(tk.END)
                    count += 1
                except Exception as e:
                    result_text.insert(tk.END, f"轉換失敗: {webp_path}, 錯誤: {e}\n")
                    result_text.see(tk.END)
    
    result_text.insert(tk.END, f"\n所有處理完成，共轉換 {count} 個檔案。\n")
    result_text.see(tk.END)

def create_window(main_window=None):
    def choose_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            folder_entry.delete(0, tk.END)
            folder_entry.insert(0, folder_selected)

    def apply_conversion():
        # 獲取資料夾路徑
        folder_path = folder_entry.get().strip()
        
        # 如果路徑為空，預設使用"下載"資料夾
        if not folder_path:
            folder_path = os.path.join(os.path.expanduser("~"), "Downloads")
            result_text.insert(tk.END, f"未指定資料夾，使用預設下載資料夾: {folder_path}\n")
            folder_entry.delete(0, tk.END)
            folder_entry.insert(0, folder_path)

        if not os.path.isdir(folder_path):
            result_text.insert(tk.END, "請輸入有效的資料夾路徑！\n")
            return
        
        # 清空結果文字區域
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"開始處理資料夾: {folder_path}\n")
        
        # 使用線程避免GUI凍結
        conversion_thread = threading.Thread(
            target=convert_webp_to_jpg, 
            args=(folder_path, result_text)
        )
        conversion_thread.daemon = True
        conversion_thread.start()

    def back_to_main():
        window.withdraw()
        main_window.deiconify()

    # 建立主視窗或子視窗
    if main_window is None:
        window = tk.Tk()
    else:
        window = tk.Toplevel(main_window)
    
    window.title("WebP 轉 JPG 工具")
    window.geometry("600x450")
    
    # 建立上方框架
    top_frame = tk.Frame(window)
    top_frame.pack(fill=tk.X, padx=20, pady=10)
    
    # 資料夾位置標籤和輸入框
    folder_label = tk.Label(top_frame, text="輸入資料夾位址:")
    folder_label.pack(side=tk.LEFT, padx=5)
    
    folder_entry = tk.Entry(top_frame, width=50)
    folder_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    # 選擇資料夾按鈕
    button_choose = tk.Button(top_frame, text="選擇資料夾", command=choose_folder)
    button_choose.pack(side=tk.RIGHT, padx=5)
    
    # 建立按鈕框架
    button_frame = tk.Frame(window)
    button_frame.pack(fill=tk.X, padx=20, pady=10)
    
    # 套用按鈕
    button_apply = tk.Button(button_frame, text="套用", command=apply_conversion, width=20)
    button_apply.pack(pady=5)
    
    # 如果這是一個子視窗，添加返回主視窗按鈕
    if main_window is not None:
        back_btn = tk.Button(window, text="返回主視窗", command=back_to_main, width=20)
        back_btn.pack(pady=10)
    
    # 結果顯示區域
    result_label = tk.Label(window, text="轉換結果:")
    result_label.pack(anchor=tk.W, padx=20)
    
    result_text = scrolledtext.ScrolledText(window, height=15)
    result_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    return window

if __name__ == "__main__":
    window = create_window()
    window.mainloop()
