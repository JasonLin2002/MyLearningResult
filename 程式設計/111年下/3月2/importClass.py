from ClassTest import Preson

class Student(Preson):
    def __init__(self,name,id):
        super().__init__(name,id)
        self.couse=None
        self.party=None
    
    def setCourse(self,courseName):
        self.couse=courseName