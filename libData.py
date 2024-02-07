from book import Book
import datetime

class LibData:
    
    @staticmethod
    def borrowBook(userId,bookId):
        import sqlite3       
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        aval = Book.checkAvailbality(bookId)
        if aval > 0 :
            today = datetime.date.today()
            today = today.strftime("%d/%m/%Y")
            c.execute("""
                      insert into borrow(userId,bookId,borrowDate,isReturned)
                      values(:uid,:bid,:bdate,0)              
                      """,{'uid':userId, 'bid':bookId, 'bdate':today})
            conn.commit()
            conn.close()                      
            Book.updateAvailibility(aval-1,bookId)
            print('Book is borrowed successfully')
            return True

        else:
            return False
    
    @staticmethod
    def returnBook(userId,bookId) :
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        today = datetime.date.today()
        today = today.strftime("%d/%m/%Y")
        c.execute(""" 
                      update borrow 
                      set isReturned = 1, returnDate = :rDate
                      where bookId = :bid
                      and userId = :uid
                      """ , {'bid':bookId, 'uid':userId, 'rDate': today})
        print("Book is returned successfully")
        conn.commit()
        conn.close() 
        LibData.calculateFine(userId, bookId)
        Book.incrementAvailability(bookId)
        
        
    
    @staticmethod
    def renewBook(userId,bookId):
        import sqlite3       
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        today = datetime.date.today()
        today = today.strftime("%d/%m/%Y")
        c.execute(""" 
                      update borrow 
                      set borrowDate = :bDate
                      where bookId = :bid
                      and userId = :uid
                      """ , {'bid':bookId, 'uid':userId, 'bDate': today})
        print("Book is renewed successfully")
        conn.commit()
        conn.close() 
        
        
    @staticmethod
    def reserveBook(bookId):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute(""" 
                      update book 
                      set reservation = reservation+1
                      where id = :bid
                      """ , {'bid':bookId})
        
        conn.commit()
        conn.close()
        print("\nBook is reserved successfully")
    
    
    @staticmethod
    def searchBook(data):
        
        import sqlite3       
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        data = '%'+data+'%'
        c.execute(""" 
                  select isbn,title,authors,pubdate,language language,pubdate from book
                  where title like :d
                  or authors like :d
                  or ISBN like :d   
                  or language like :d
                  or pubdate like :d
                  """,{'d':data})
        result = c.fetchall() 
        print("\n#############################")
        print('Search Results: ')
        i = 1
        for book in result:
            print(f"{i} - {book[0]} - {book[1]} - {book[2]} - {book[3]} - {book[4]}")
            i = i +1
        conn.commit()
        conn.close() 
        
    @staticmethod
    def calculateFine(userId,bookId):
        
        import sqlite3       
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute(""" 
                  select borrowDate,returnDate from borrow
                  where userId = :uid
                  and bookId = :bid
               
                  """,{'uid':userId,'bid' : bookId})
        result = c.fetchone()
        
        borrowDate = result[0]
        returnDate = result[1]
        bDate = datetime.datetime.strptime(borrowDate,"%d/%m/%Y")
        rDate = datetime.datetime.strptime(returnDate,"%d/%m/%Y")
        delta = rDate - bDate
        delta = delta.days
        
        if delta <= 7:
            pass
        else:
            fineDays = delta - 7
            fine = fineDays*2
            print(f"""You returned the book after {delta} days.
The fine for everyday delay more than 7 days is 2 pound.
You have to pay {fine} pounds.""")
            
            #Updating fine amount in database
            c.execute(""" 
                      update user
                      set fines = fines+ :new
                      where Id = :uid
                      """ , {'new':fine, 'uid': userId})         
            conn.commit()
            conn.close()
    
    
    
    @staticmethod
    def getUserIdByUsername(username):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute("""
                  select id from user
                  where username = :us         
                  """,{'us':username})
        result = c.fetchone()
        
        conn.commit()
        conn.close()
        return result[0]
