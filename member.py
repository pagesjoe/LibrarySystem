from book import Book
from libData import LibData

class Member:
    
    def __init__(self,Id):
        self.__Id = Id
        
        
    @property
    def Id(self):
        return self.__Id
    
    @Id.setter
    def Id(self,value):
        self.__Id = value
    
    #Polymorphism method
    def printInfo(self):
        print("Welcome to the application")
    
    
    
    def borrow(self):
        #Checking first if the user has borrowed 5 books
        numBorrBooks = self.getNumBorrowedBooks()
        
        if numBorrBooks < 5:
            while True:
                isbn = input('Please enter isbn: ')
                bookId = Book.getBookIdByIsbn(isbn)
                
                #Check if there is a book with this ISBN
                if not bookId == 0:
                    break
                else:
                    print("No book with this ISBN")
                
            #Check if the book is already booked before by the user
            if self.checkBookIsBorrowedByUser(bookId):
                print("You already borrowed this book before")
            else:
                #Call the LibData borrowBook function 
                if LibData.borrowBook(self.Id, bookId):
                    #If the book is borrowed successfully, increment the number
                    #of borrowed books by the user
                    newNum = numBorrBooks+1
                    self.updateNumBorrowedBooks(newNum)
                else:
                    print("Sorry!! You already reached maximum number of borrowed books")
        
    
    
    
    def renew(self):
        
        isbn = input('Please enter isbn: ')
        bookId = Book.getBookIdByIsbn(isbn)
        
        if self.checkBookIsBorrowedByUser(bookId):
            
            if Book.bookIsReserved(bookId):
                print("Sorry! The book is reserved. You can not renew the book.")
            else:
                LibData.renewBook(self.Id, bookId)
                
        else:
            print("You have no borrowed book with that isbn")
    
    
    
    def reserve(self):
        while True:
            isbn = input('Please enter isbn: ')
            bookId = Book.getBookIdByIsbn(isbn)
            
            if not bookId==0:
                
                if Book.checkAvailbality(bookId)==0:
                    LibData.reserveBook(bookId)
                else:
                    print("The book is available to borrow")
                    break
            else:
                print("\nNo book with this ISBN")
    
    
    
    def payFine(self):
        import sqlite3       
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        
        c.execute(""" 
                  select fines from user
                  where Id = :uId
                  """,{'uId':self.Id})
        res = c.fetchone()
        fines = res[0]
        
        if fines>0:
            print(f"Your total fine amount is: {fines}")
            
            while True:
                try:
                    payment = int(input("Please enter the amount you want to pay: "))
                except:
                    print("\nError try again")
                else:
                    if payment>fines:
                        print("\nPlease enter sufficient amount")
                    else:
                        break
                
            print(f"You paid {payment} pounds")
            
            newFines = fines-payment
            print(f"Your new total fine amount is: {newFines}")
            
            c.execute("""
                      update user
                      set fines = :new
                      """,{'new': newFines})
            conn.commit()
            conn.close()
        else:
            print("You dont have any fines")
        
        
        
    
    def returnBook(self):
        
            isbn = input("Please enter the book isbn: ")
            bookId = Book.getBookIdByIsbn(isbn)
            
            #Checking first if user already borow a book with this isbn
            if self.checkBookIsBorrowedByUser(bookId):
                LibData.returnBook(self.Id,bookId)
                
                #Decrease number of borrowed books of the user by 1
                newNum = self.getNumBorrowedBooks()-1
                self.updateNumBorrowedBooks(newNum)
            else:    
                print("You have no borrowed book with that isbn")

    
    def searchBook(self):
        data = input('Please enter search data: ')
        LibData.searchBook(data)
        
        
    
    def getBorrowedBook(self):
        import sqlite3       
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        
        c.execute(""" 
                  select book.isbn,book.title,borrow.isReturned from book,borrow
                  where borrow.bookId = book.Id
                  and borrow.isReturned = 0
                  and borrow.userId = :uId
                  """,{'uId':self.Id})
                  
        # books is the list of all books with this specification           
        books = c.fetchall()
        if not books:
            print('No borrowed books!')
            print('')
        else:   
            print('')
            print('*********************')
            print('* List Of Borowed Book*')
            print('*********************')
            for book in books:
                print(f"{book[0]} - {book[1]}")
            print('')
        
        conn.commit()
        conn.close()   
        
    
    def getNumBorrowedBooks(self):
        import sqlite3       
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        
        c.execute(""" 
                  select BorrowedBooks from user
                  where id = :uid
                  """, {'uid':self.Id})
        return c.fetchone()[0]
    
    
    def updateNumBorrowedBooks(self,newNum):
        import sqlite3       
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        
        c.execute(""" 
                  update user
                  set BorrowedBooks = :num
                  where Id = :uId
                  """,{'num':newNum, 'uId':self.Id})
                  
        conn.commit()
        conn.close()
    
     
    def checkBookIsBorrowedByUser(self,bookId):
        import sqlite3       
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        
        c.execute(""" 
                  select * from borrow
                  where bookId = :bid
                  and userId = :uid
                  and isReturned = 0
                  """ , {'bid':bookId, 'uid':self.Id})
        result = c.fetchone()          
        conn.commit()
        conn.close()
        
        if result == None:
            return False
        else:    
            return True
    
    def menu(self):
            
            while True:
                print("""
                  1. List Of the borrowed Books
                  2. Borrow a Book
                  3. Search
                  4. Return a book
                  5. Renew a book
                  6. Reserve a book
                  7. Pay Fine
                  
                  q. quit
                  """)
                choice = input("select your choice: ")
                f = {
                "1": self.getBorrowedBook,
                "2": self.borrow,
                "3": self.searchBook,
                "4": self.returnBook,
                "5": self.renew,
                "6": self.reserve,
                "7": self.payFine,
                "q": 'q'
                }.get(choice,None)
                
                if f == 'q':
                    break
                if f == None:
                    print("Error, Try Again..")
                else:
                    f()
                    
                    
    def printInfo(self):
        print(f"Your Id is {self.Id}")
    