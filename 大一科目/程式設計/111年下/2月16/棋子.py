class Chess:
    def __init__(self, name, color, strength):
        self.name = name
        self.color = color
        self.strength = strength

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def setStrength(self, strength):
        self.strength = strength

    def getStrength(self):
        return self.strength

    def showInfo(self):
        print("名字:", self.name)
        print("顏色:", self.color)
        print("強度:", self.strength)
if __name__ == '__main__':
    Chess1=Chess('King',"黑",92)
    Chess1.showInfo()

    Chess2=Chess('Queen',"白",82)
    Chess2.showInfo()

    Chess3=Chess('Bishop',"黑",72)
    Chess3.showInfo()