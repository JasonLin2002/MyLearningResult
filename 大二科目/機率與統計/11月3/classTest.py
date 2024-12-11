import pandas as pd

# 讀取Excel文件
file_path = 'GolfTest.xlsx'
df = pd.read_excel(file_path, names=['Yards'])

# 計算平均飛行距離
average_distance = df['Yards'].mean()

# 輸出結果
print(f"平均飛行距離: {average_distance} 碼")

# 檢定是否等於295碼
target_distance = 295
if average_distance == target_distance:
    print("高爾夫球的平均飛行距離等於295碼。")
else:
    print("高爾夫球的平均飛行距離不等於295碼。")