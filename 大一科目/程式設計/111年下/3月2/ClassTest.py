class Person:
    def __init__(self,name,id):
        self.__name=name
        self.__id=id
    
    @property
    def name(self):
        return 'No deta!'
    
    @name.setter
    def setName(self,newName):
        self.__name=newName
    
    @name.getter
    def getName(self):
        return self.__name