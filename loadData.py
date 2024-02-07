# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:53:27 2023

@author: TOSHIBA
"""

import json
import sqlite3


conn = sqlite3.connect("libdb.db")
c = conn.cursor()


with open("books.json", encoding="utf-8" ) as fd:
    books = json.load(fd)
 
for book in books:    
    c.execute("""INSERT INTO book(isbn,title,authors,available,Language,PubDate)
                  VALUES(:is,:ti,:au,:av,:lan,:pd)"""
                  ,{'is':book['isbn'], 'ti': book['title'], 'au' : book['authors']
                    , 'av': 3, 'lan': book['language_code'], 'pd': book['publication_date']})


conn.commit()
conn.close()
