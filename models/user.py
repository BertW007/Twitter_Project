from .crypto import password_hash


class User(object):
    """
    This class represents User in database.
    """
    # __id = None
    # username = None
    # __hashed_password = None
    # email = None
    
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
        self.__hashed_password = password_hash(password, salt)
        
    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """
                INSERT INTO Users(name,hashed_password,email)
                VALUES('{}','{}','{}');""".format(self.username,
                                                  self.hashed_password,
                                                  self.email)
                
            cursor.execute(sql)
            self.__id = cursor.lastrowid
            return True
        else:
            sql = "UPDATE Users SET name='{}',email='{}',hashed_password='{}'" \
                  " WHERE user_id={};".format(self.username,
                                              self.email,
                                              self.hashed_password,
                                              self.__id)
            print(sql)
            cursor.execute(sql)
            return True
    
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
    
    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT user_id, name, email, hashed_password FROM Users"
        ret = []
        result = cursor.execute(sql)
        data = cursor.fetchall()

        for row in data:
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.username = row[1]
            loaded_user.email = row[2]
            loaded_user.__hashed_password = row[3]
            ret.append(loaded_user)
        return ret
    
    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE user_id={}".format(self.__id)
        cursor.execute(sql)
        self.__id = -1
        return True
