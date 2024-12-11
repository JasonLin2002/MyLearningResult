class Array:
    def __init__(self, n: list, size: int):
        self.array = [None] * size
        self.length = len(n)
        self.size = size
        if self.length > size:
            self.length = size
        for i in range(self.length):
            if i < size:
                self.array[i] = n[i]
            else:
                break

    def traverse(self):
        arr_1 = self.array
        length = self.length

        print("Traverse:")
        for i in range(length):
            print("[{}]: {}".format(i, arr_1[i]))

    def insert(self, key: int, index: int):
        arr_1 = self.array
        size = self.size
        length = self.length
        if length >= size:
            print("The array is full!")
        else:
            if index < 0:
                print("Error index!")
            elif index < length:
                for i in range(length-1, index-1, -1):
                    arr_1[i+1] = arr_1[i]
                arr_1[index] = key
                self.length += 1
            else:
                arr_1[length] = key
                self.length += 1

    def delete(self, index: int):
        arr_1 = self.array
        length = self.length
        if length <= 0:
            print("The array is empty!")
        else:
            if index < 0:
                print("Error index!")
            elif index < length:
                for i in range(index, length-1):
                    arr_1[i] = arr_1[i+1]
                arr_1[length-1] = None
                self.length -= 1

    def search(self, key: int) -> int:
        arr_1 = self.array
        length = self.length
        for i in range(length):
            if key == arr_1[i]:
                return i
        return -1

    def update(self, key: int, index: int):
        arr_1 = self.array
        length = self.length
        if index < 0 or index >= length:
            print("Error index!")
        else:
            arr_1[index] = key

if __name__ == "__main__":
    arr_1 = Array([1, 2, 3], 5)
    arr_1.traverse()
    arr_1.insert(4, 3)
    arr_1.traverse()
    arr_1.delete(3)
    arr_1.traverse()
    arr_1.update(100, 0)
    arr_1.traverse()
    print("index:", arr_1.search(5))
    print("index:", arr_1.search(100))
