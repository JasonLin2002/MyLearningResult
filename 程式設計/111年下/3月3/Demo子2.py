from Demo父 import Car

class Scooter(Car):
    def __init__(self, product_name, license_plate, car_type, load_capacity, wheel_number):
        super().__init__(product_name, license_plate, car_type)
        self.__load_capacity = load_capacity
        self.__wheel_number = wheel_number

    def get_load_capacity(self):
        return self.__load_capacity

    def set_load_capacity(self, load_capacity):
        self.__load_capacity = load_capacity

    def get_wheel_number(self):
        return self.__wheel_number

    def set_wheel_number(self, wheel_number):
        self.__wheel_number = wheel_number

    def horsepower():
        return '帥帥檔車'
    
    def print_info(self):
        super().print_info()
        print("Load Capacity:", self.__load_capacity)
        print("Wheel Number:", self.__wheel_number)
        print(Scooter.horsepower())
    