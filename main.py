from user import User
from member import Member
from librarian import Librarian
from student import Student
from staff import Staff

while True:
    
    choice = input("""Welcome to BCU Library System
          1. login
          2. Register
select your choice: """)
          
    if choice == '1':
       
        # Login
        uid = input("Enter username: ")
        pswd = input("Enter your password: ")
        loginResult = User.login(uid, pswd)
        
        if loginResult['userExists'] == True:
            print("#############################")
            print(f"Welcome to BCU Library System \n{loginResult['Name']}....")
            
            if loginResult['Role'] == 'student':
                student = Student(loginResult['Id'],loginResult['Category'])
                student.printInfo()
                student.menu()
                
            elif loginResult['Role'] == 'staff':
                staff = Staff(loginResult['Id'],loginResult['Category'])
                staff.printInfo()
                staff.menu()
                
            if loginResult['Role'] == 'lib':
                lib = Librarian(loginResult['Id'])
                lib.menu()
                
        else:
            print("Login failure")
    
    elif choice == '2':
        #Register
        name = input("Type your name: ")
        userName = input("Type your username: ")
        password = input("Type your password: ")
        
        while True:
            roleChoice = input(""""Choose your role:
                         1. Student
                         2. Staff
    select your choice: """)
            if roleChoice == '1':
                role = 'student'
                category = input("Please type your class number:")
                break
            elif roleChoice == '2':
                role = 'staff'
                category = input("Please type your department:")
                break
            else:
                print("\nPlease type a proper choice")
        
        #Creating user in the database
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute("""
        INSERT INTO User(Name,UserName,Password,Role,Category)
        VALUES (:name, :userName, :password, :role, :cat)
        """,{'name':name, 'userName':userName, 'password':password, 'role':role, 'cat':category})
        conn.commit()
        conn.close()
        
        print("""
##########################
Account Registered Successfully
""")
        
    else:
        print("\nPlease type proper choice")
    