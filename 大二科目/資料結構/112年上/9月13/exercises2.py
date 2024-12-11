class Course:
    def __init__(self, name:str, teacher:str, location:str, time:str):
        self.name = name
        self.teacher = teacher
        self.location = location
        self.time = time
    
    def showInfo(self):
        print("課程資訊:")
        print("---"*5)
        print("課程名稱: ", self.name)
        print("教師: ", self.teacher)
        print("地點 :", self.location)
        print("時間: ", self.time)
        print("---"*5)

class Student:
    def __init__(self, name:str, id:str, gender:str, grade:int):
        self.name = name
        self.id = id
        self.gender = gender
        self.grade = grade
        self.course = []
    
    def addCourse(self, course:Course):
        self.course.append(course)
    
    def showInfo(self):
        print("---"*5)
        print("姓名: ", self.name)
        print("學號 :", self.id)
        print("性別: ", self.gender)
        print("年級: ", self.grade)
        print("課程: ")
        for i in range(len(self.course)):
            print("{} " .format(i)+self.course[i].name)
        if len(self.course) == 0:
            print("無課程")
        print("---"*5)

if __name__ == "__main__":
    course1 = Course("線性代數", "t1", "202教室", "週一 03-04")
    course1.showInfo()
    
    course2 = Course("資料結構", "t2", "201教室", "週二 06-07")
    course2.showInfo()

    course3 = Course("微積分", "t3", "103教室", "週三 01-02")
    course3.showInfo()
    
    course4 = Course("物件導向程式設計", "t4", "301教室", "週四 06-08")
    course4.showInfo()
    
    course5 = Course("網際網路概論", "t5", "203教室", "週五 01-02")
    course5.showInfo()
    
    student1 = Student("傑克", "000001", "男性", 1)
    student1.addCourse(course1)
    student1.addCourse(course3)
    student1.addCourse(course5)
    student1.showInfo()
    
    student2 = Student("差學生", "00002", "男性", 4)
    student2.showInfo()
    
    student3 = Student("好學生", "00003", "女性", 2)
    student3.addCourse(course1)
    student3.addCourse(course2)
    student3.addCourse(course3)
    student3.addCourse(course4)
    student3.addCourse(course5)
    student3.showInfo()
