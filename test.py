from models.user import User
from mysql.connector import connect
from mysql.connector.errors import ProgrammingError

user = 'root'
password = 'coderslab'
host = 'localhost'
database = 'twitter_db'

def testCreateUser():
    new_user = User()
    new_user.name = 'frodo'
    new_user.email = 'fb@ring.com'
    new_user.set_password('precious')
    
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
            read_user = User.load_user_by_id(cursor,2)
            print(read_user.username, '-' , read_user.email)
        except AttributeError:
            print('There is no such record in database...')
            
        cnx.commit()           
        cursor.close()
        cnx.close()
        print('Disconnected...')
         
    except TypeError:
            print("Not connected...")
    
    


if __name__ == "__main__":
    testReadUser()