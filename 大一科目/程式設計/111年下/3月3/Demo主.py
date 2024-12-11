from Demo父 import Car
from Demo子 import Truck
from Demo子2 import Scooter

if __name__=="__main__":
    car_list = []

    car1 = Car("Toyota Car", "ABC-1234", "Sedan")
    car2 = Truck("脫拉庫", "ABC-1234", "傾卸框式大貨車", "15頓", "8輪")
    car3 = Scooter("honda D123312", "DEF-5678", "檔車", "200kg", "2輪")

    car_list.append(car1)
    car_list.append(car2)
    car_list.append(car3)


    for car in car_list:
        car.print_info()
        print()