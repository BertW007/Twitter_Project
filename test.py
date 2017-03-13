from models.user import User
from mysql.connector import connect
from mysql.connector.errors import ProgrammingError

user = 'root'
password = 'coderslab'
host = 'localhost'
database = 'twitter_db'

def testCreateUser():
    new_user = User()
    new_user.name = 'gollum'
    new_user.email = 'smeagol@fish.com'
    new_user.set_password('gollum')
    
    try:
        cnx = connect(user=user, password=password, host=host, database=database)
        print("Connected...")
        cursor = cnx.cursor()  
              
        new_user.save_to_db(cursor)
        
        cnx.commit()           
        cursor.close()
        cnx.close()
        print('Disconnected...')
         
    except ProgrammingError:
            print("Not connected...")
    
def testReadUser():
    
    try:
        cnx = connect(user=user, password=password, host=host, database=database)
        print("Connected...")
        cursor = cnx.cursor()  
        try:      
            read_user = User.load_user_by_id(cursor,5)
            print(read_user.username, '-' , read_user.email)
        except AttributeError:
            print('There is no such record in database...')
            
        cnx.commit()           
        cursor.close()
        cnx.close()
        print('Disconnected...')
         
    except TypeError:
            print("Not connected...")
            
def testAllUsers():
#     i = None
    
    try:
        cnx = connect(user=user, password=password, host=host, database=database)
        print("Connected...")
        cursor = cnx.cursor()  
        try:      
            users = User.load_all_users(cursor)
            for i in users:
                print(i.username, '-' , i.email)
        except AttributeError:
            print('There is no such record in database...')
            
        cnx.commit()           
        cursor.close()
        cnx.close()
        print('Disconnected...')
         
    except TypeError:
            print("Not connected...")
    
    


if __name__ == "__main__":
    testAllUsers()