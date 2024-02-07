class Book:
    

    
    def updateBook(bookId, title, authors):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute(""" 
                      update book set
                      title = :titl, authors = :auth
                      where id = :bid
                      """ , {'titl' : title, 'bid':bookId, 'auth' : authors})
        print("Book is modified successfully")
        conn.commit()
        conn.close()
        
        
    def createBook(isbn, title, authors,available):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute(""" 
                      INSERT INTO book (isbn, title, authors, available)
                      VALUES (:is, :tit, :auth, :avail)
                      """ , {'is' : isbn, 'tit':title, 'auth' : authors,
                      'avail' : available})
        print("Book is created successfully")
        conn.commit()
        conn.close()
        
     
        
    def viewBook(bookId):
        import sqlite3       
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        
        c.execute(""" 
                  select isbn,title,authors,available, reservation from book
                  where Id = :is                  
                  """,{'is':bookId})
        result = c.fetchone() 
        print(f"isbn: {result[0]}\nTitle: {result[1]}\nAuthors: {result[2]}\nAvailable copies: {result[3]}\nReservations: {result[4]}")
        conn.commit()
        conn.close() 
        
    
    def checkAvailbality(bookId):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()


        c.execute("""
                  select available from Book
                  where id = :bid          
                  """,{'bid':bookId})

        ava = c.fetchone()[0]
        conn.close()
        return ava
    
    def updateAvailibility(number, bookId):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute(""" 
                      update book set
                      available = :nava
                      where id = :bid
                      """ , {'nava' : number, 'bid':bookId})
        
        conn.commit()
        conn.close()
        
        
    def incrementAvailability(bookId):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute(""" 
                      update book 
                      set available = available+1
                      where id = :bid
                      """ , {'bid':bookId})
        
        conn.commit()
        conn.close()
    
    
    def bookIsReserved(bookId):
        
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute("""
                  select reservation from Book
                  where Id = :bid          
                  """,{'bid':bookId})
        result = c.fetchone()[0]
        conn.commit()
        conn.close()
        
        if result >0:
            return True
        else:
            return False
    
    
    @staticmethod
    def getBookIdByIsbn(isbn):
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute("""
                  select id from Book
                  where isbn = :is          
                  """,{'is':isbn})
        result = c.fetchone()
        
        conn.commit()
        conn.close()
        if not result:
            return 0
        else:
            return result[0]
