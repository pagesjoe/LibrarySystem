from member import Member

class Student(Member):
    
    def __init__(self, Id, classNo):
        super().__init__(Id)
        self.classNo = classNo
        
    def printInfo(self):
        print(f"""Class number: {self.classNo}""")