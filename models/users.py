from models.crypto.crypto import *

class User(object):
   
    __id = None
    username = None
    __hashed_password = None
    email = None
    
    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""
        
    @property
    def id(self):
        return self.__id
    
    @property
    def hashed_password(self):
        return self.__hashed_password
    
    def set_password(self, password, salt):
        self.__hashed_password = \
        password_hash(password, salt)
        
    def save_to_db(self, cursor):
        if self.__id == -1:
            sql_guery = """
                INSERT INTO Users(name,hashed_password,email)
                VALUES('{}','{}','{}');""".format(self.name,self.hashed_password,self.email)
                
            cursor.execute(sql_guery)
            self.__id = cursor.lastrowid
            return True
        else:
            return False
                