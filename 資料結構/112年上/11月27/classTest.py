def count_letters(input_text):
    # 初始化一個空的字母計數字典
    letter_count = {}

    # 遍歷輸入的文字
    for char in input_text:
        # 只考慮字母，忽略空格、標點符號等
        if char.isalpha():
            # 將字母轉為小寫，以區分大小寫
            char = char.lower()
            # 更新字母計數字典
            letter_count[char] = letter_count.get(char, 0) + 1

    return letter_count

# 接收使用者輸入的文字
user_input = input("請輸入一段文字：")

# 計算字母使用次數
result = count_letters(user_input)

# 顯示結果
print("字母使用次數：")
for letter, count in result.items():
    print(f"{letter}: {count}次")
