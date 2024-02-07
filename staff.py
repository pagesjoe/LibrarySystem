from member import Member

class Staff(Member):
    
    def __init__(self, Id, dep):
        super().__init__(Id)
        self.dep = dep
        
    def printInfo(self):
        print(f"""Department: {self.dep}""")