from models.crypto import *

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
    
    def set_password(self, password):
        salt=generate_salt()
        self.__hashed_password =password_hash(password, salt)
        
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
    
    @staticmethod
    def load_user_by_id(cursor, id):
        sql = "SELECT user_id, name, email, hashed_password FROM Users WHERE user_id={}".format(id)
        result = cursor.execute(sql)
        data = cursor.fetchone()
         
        if data is not None:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None
    
                            
                