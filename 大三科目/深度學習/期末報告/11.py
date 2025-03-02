import os
import opencc

# 遞迴處理資料夾內的檔案名稱
# 假設亂碼的檔案名是 GB2312 編碼，轉換為 UTF-8 並翻譯成繁體

def fix_and_convert_filenames(directory):
    converter = opencc.OpenCC('s2t')  # 簡體轉繁體配置
    for root, dirs, files in os.walk(directory):
        for name in files + dirs:
            try:
                # 嘗試將檔案名從 GB2312 轉換為 UTF-8
                fixed_name = name.encode('latin1').decode('gb2312')
                # 將簡體轉為繁體
                traditional_name = converter.convert(fixed_name)

                original_path = os.path.join(root, name)
                fixed_path = os.path.join(root, traditional_name)

                # 重命名檔案或資料夾
                os.rename(original_path, fixed_path)
                print(f"Renamed: {original_path} -> {fixed_path}")
            except (UnicodeEncodeError, UnicodeDecodeError):
                print(f"Skipping: {name} (cannot decode)")

if __name__ == "__main__":
    # 使用者輸入資料夾路徑
    directory = input("Enter the directory to fix filenames: ")
    if os.path.exists(directory):
        fix_and_convert_filenames(directory)
        print("Finished processing filenames.")
    else:
        print("The specified directory does not exist.")
