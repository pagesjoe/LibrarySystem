from book import Book
from libData import LibData
from member import Member
import datetime

class Librarian:
    
    def __init__(self,Id):
        self.__Id = Id
        
        
    @property
    def Id(self):
        return self.__Id
    
    @Id.setter
    def Id(self,value):
        self.__Id = value
    
    
    def updateBook(self):
        while True:
            isbn = input('Please enter isbn of book that you want to update: ')
            bookId = Book.getBookIdByIsbn(isbn)
            
            if not bookId == 0:
                title = input('Please enter the new title: ')
                authors = input('Please enter the new authors: ')
                Book.updateBook(bookId, title, authors)
                break
            else:
                print("\nNo book with this Isbn")
        
    
    def createBook(self):
        isbn = input('Please enter isbn of the book: ')
        title = input('Please enter the title: ')
        authors = input('Please enter the authors: ')
        while True:
            try:
                available = int(input('Please enter the number of copies: '))
            except:
                print("\nPlease type a valid number")
            else:
                Book.createBook(isbn, title, authors,available)
                break
    
    
    
    def returnBook(self):
        while True:
            isbn = input('Please enter isbn of book that you want to return: ')
            bookId = Book.getBookIdByIsbn(isbn)
            
            if not bookId == 0:
                username = input('Please enter username: ')
                while True:
                    try:
                        userId = LibData.getUserIdByUsername(username)
                        break
                    except:
                        print("Please type proper username")
                    else:
                        LibData.returnBook(userId, bookId)
                        break
            else:
                print("\nNo book with this Isbn")
        
    
    
    def viewBook(self):
        while True:
            isbn = input('Please enter isbn of book: ')
            bookId = Book.getBookIdByIsbn(isbn)
            if not bookId == 0:
                Book.viewBook(bookId)
            else:
                print("Please enter a proper isbn")
    
    def searchBook(self):
        data = input('Please enter search data: ')
        LibData.searchBook(data)
    
    def getBorrowedBookforUser(self):
        userId = input('Please enter the user ID: ')
        member = Member(userId)
        member.getBorrowedBook()
        
        
    
    def viewReports(self):
        sDate = input("Please enter start date in the format dd/mm/yyyy: ")
        startDate = datetime.datetime.strptime(sDate,"%d/%m/%Y")
        eDate = input("Please enter end date in format dd/mm/yyyy: ")
        endDate = datetime.datetime.strptime(eDate,"%d/%m/%Y")
        
        import sqlite3       
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute("""
                      select borrowDate,Id from borrow
                  """)
        result = c.fetchall()
        
        print(f" \n####################### \nList of borrowed books from {sDate} to {eDate}: \n")
        
        i = 1
        for res in result:
            date = res[0]
            borrDate = datetime.datetime.strptime(date,"%d/%m/%Y")
            if endDate>=borrDate>=startDate:
                c.execute("""
                              select book.isbn, book.title, borrow.borrowDate from book,borrow
                              where book.Id = borrow.bookId
                              and borrow.Id = :bid
                              """,{'bid':res[1]})
                book = c.fetchone()
                print(f"\n{i} - {book[0]} - {book[1]} \nborrow date: {book[2]}")
                i=i+1
        
        print("############################")    
        
        conn.commit()
        conn.close()                      
    

        
    def menu(self):
            while True:
                print("""
                  1. update books
                  2. create new book
                  3. return a book
                  4. view Book
                  5. get user borrowed books
                  6. view reports
                  q. quit
                  """)
                choice = input("select your choice: ")
                f = {
                "1": self.updateBook,
                "2": self.createBook,
                "3": self.returnBook,
                "4": self.viewBook,
                "5": self.getBorrowedBookforUser,
                "6": self.viewReports,
                "q": 'q'}.get(choice,None)
                if f == 'q':
                    break
                if f == None:
                    print("Error, Try Again..")

                else:
                    f()
   