import os

# 設定主要的資料夾路徑
DATASET_DIR = r"C:\Users\jk121\Documents\Code\LargeData\Model_for_English_Words_test"  # 替換成你的資料夾路徑

def rename_files_in_folders(dataset_dir):
    """ 遍歷所有子資料夾並將檔案重新命名為 img1.jpg, img2.jpg... """
    # 遍歷主資料夾中的所有子資料夾 (A, B, C...)
    for folder in sorted(os.listdir(dataset_dir)):
        folder_path = os.path.join(dataset_dir, folder)
        
        # 確保是資料夾
        if os.path.isdir(folder_path):
            print(f"正在處理資料夾: {folder}")
            
            # 遍歷每個檔案並重新命名
            for idx, file in enumerate(sorted(os.listdir(folder_path))):
                old_file_path = os.path.join(folder_path, file)
                
                # 檢查是否是檔案
                if os.path.isfile(old_file_path):
                    new_file_name = f"img{idx+1}.jpg"
                    new_file_path = os.path.join(folder_path, new_file_name)
                    
                    # 重新命名檔案
                    os.rename(old_file_path, new_file_path)
                    print(f"  {file} -> {new_file_name}")

    print("所有檔案重新命名完成！")

# 執行函數
rename_files_in_folders(DATASET_DIR)
