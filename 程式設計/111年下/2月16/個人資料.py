class Person:
    def __init__(self, name, id, height, weight, gender):
        self.name = name
        self.id = id
        self.height = height
        self.weight = weight
        self.gender = gender

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setHeight(self, height):
        self.height = height

    def getHeight(self):
        return self.height

    def setWeight(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

    def setGender(self, gender):
        self.gender = gender

    def getGender(self):
        return self.gender

    def showInfo(self):
        print("姓名:", self.name)
        print("身份證字號:", self.id)
        print("身高:", self.height)
        print("體重:", self.weight)
        print("性別:", self.gender)

    def getStdBMI(self):
        return self.weight/(self.height/100) ** 2

if __name__ == '__main__':
    Person1=Person('阿明',"A132186663",172,72,'男')
    Person1.showInfo()