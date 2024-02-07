class User:
    
    def __init__(self,Id):
        self.__Id = Id
     
    @staticmethod    
    def login(username,password):
        """
        This function check whether a user is exist in database or not. 

        Parameters
        ----------
        username : string
            The username should input by user
        password : string
            The password should input by user

        Returns
        -------
        dict
            this function returns a dictionary. if rocerd be fined it return all the neccessary information,
            if no it return the key 'IsExist' and value of False.

        """
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute(""" 
                  SELECT Id,Name,Role,category from User
                  where UserName = :uName
                  and Password = :pass
                  """,{'uName':username , 'pass':password})
        result = c.fetchone()
        
        if not result:
            return {'userExists' : False}
        else:
            return {'userExists' : True , 'Id': result[0] , 'Name': result[1], 
                    'Role': result[2], 'Category' : result[3]}
        conn.commit()
        conn.close()
    
    def register():
        import sqlite3
        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()
        c.execute("""
        INSERT INTO User
        VALUES (value1, value2, value3)
        """)
    

