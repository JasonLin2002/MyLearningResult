from hero import Hero

def main(hero1,hero2):
    hero1= Hero("術士", 10, 100, 50, 20)
    hero2= Hero("戰士", 10, 200, 40, 20)

if __name__=='__main__':
    hero1.showInfo()
    hero2.showInfo()
