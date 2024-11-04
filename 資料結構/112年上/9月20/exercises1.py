class InsertionSort:
    def __init__(self, number):
        self.number = number

    def sort(self):
        n = len(self.number)
        for i in range(1, n):
            key = self.number[i]
            j = i - 1
            while j >= 0 and self.number[j] > key:
                self.number[j + 1] = self.number[j]
                j -= 1
            self.number[j + 1] = key
    
    def inv(self):
        n = len(self.number)
        for i in range(1, n):
            key = self.number[i]
            j = i - 1
            while j >= 0 and self.number[j] < key:  
                self.number[j + 1] = self.number[j]
                j -= 1
            self.number[j + 1] = key

if __name__ == "__main__":
    number = [2,5,3,8,9,1,0,4,6,7]
    Insert = InsertionSort(number)
    Insert.sort()
    print(Insert.number)
    Insert.inv()
    print(Insert.number)
