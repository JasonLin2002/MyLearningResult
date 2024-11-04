input_str = input("輸入數字：")
Number = [int(x) for x in input_str.split()]

def insertion_sort(Number):
    n = len(Number)
    for i in range(1, n):
        key = Number[i]
        j = i - 1
        while j >= 0 and Number[j] > key:
            Number[j + 1] = Number[j]
            j -= 1
        Number[j + 1] = key

def insertion_sort_descending(Number):
    n = len(Number)
    for i in range(1, n):
        key = Number[i]
        j = i - 1
        while j >= 0 and Number[j] < key:  
            Number[j + 1] = Number[j]
            j = j - 1
        Number[j + 1] = key

insertion_sort(Number)
print("由小排到大:", Number)

insertion_sort_descending(Number)
print("由大排到小:", Number)