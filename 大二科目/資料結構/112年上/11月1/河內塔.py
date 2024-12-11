from ex1 import Stack



class hanoiTower:
    def __init__(self, n:int, pos:int):
        if (-1 < pos < 3):
            self.Towers = []
            self.n = n
            self.pos = pos
            for i in range(3):
                self.Towers.append(Stack())
            for i in range(n):
                self.Towers[pos].push(n-i)
            for i in range(3):
                print("Tower{}: ".format(i), end="")
                self.Towers[i].printAllItem()
        else:
            print("Error pos")

    def __move(self, start:int, goal:int, n:int):
        if (n > 1):
            temp = 3-(start+goal)
            self.__move(start, temp, n-1)
            self.__move(start, goal, 1)
            self.__move(temp, goal, n-1)
        else:
            move_data = self.Towers[start].pop()
            self.Towers[goal].push(move_data)
    
    def move(self, start:int, goal:int):
        self.__move(start, goal, self.n)
        print("After move:")
        for i in range(3):
            print("Tower{}: ".format(i), end="")
            self.Towers[i].printAllItem()

if __name__ == "__main__":
    h1 = hanoiTower(5, 1)
    h1.move(1, 0)