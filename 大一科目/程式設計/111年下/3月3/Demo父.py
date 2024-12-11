class Car:
    def __init__(self, name, plate, type):
        self.__product_name = name
        self.__license_plate = plate
        self.__car_type = type

    @property
    def name(self):
        return '沒輸入!'

    @name.setter
    def set_product_name(self, product_name):
        self.__product_name = product_name
    
    @name.getter
    def get_product_name(self):
        return self.__product_name

    @property
    def plate(self):
        return '沒輸入!'
    
    @plate.getter
    def get_license_plate(self):
        return self.__license_plate

    @plate.setter
    def set_license_plate(self, license_plate):
        self.__license_plate = license_plate

    @property
    def type(self):
        return '沒輸入!'
    
    @type.getter
    def get_car_type(self):
        return self.__car_type
    
    @type.setter
    def set_car_type(self, car_type):
        self.__car_type = car_type

    def print_info(self):
        print("Product Name:", self.__product_name)
        print("License Plate:", self.__license_plate)
        print("Car Type:", self.__car_type)
