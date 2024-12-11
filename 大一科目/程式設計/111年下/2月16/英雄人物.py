class Hero:
    def __init__(self, name, level, hp, mp, attack):
        self.name = name
        self.level = level
        self.hp = hp
        self.mp = mp
        self.attack = attack

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setLevel(self, level):
        self.level = level

    def getLevel(self):
        return self.level

    def setHP(self, hp):
        self.hp = hp

    def getHP(self):
        return self.hp

    def setMP(self, mp):
        self.mp = mp

    def getMP(self):
        return self.mp

    def setAttack(self, attack):
        self.attack = attack

    def getAttack(self):
        return self.attack

    def showInfo(self):
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print(f"HP: {self.hp}")
        print(f"MP: {self.mp}")
        print(f"Attack: {self.attack}")

if __name__ == '__main__':
  hero1 = Hero("戰士", 10, 100, 50, 20)
  hero2 = Hero("牧師", 8, 80, 120, 15)
  hero3 = Hero("盜賊", 12, 120, 30, 25)
  
  hero1.setName("瓦里安")
  hero2.setName("費倫")
  hero3.setName("瓦麗拉")
  
  hero1.showInfo()
  hero2.showInfo()
  hero3.showInfo()
