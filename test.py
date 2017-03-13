from models.user import User
from mysql.connector import connect
from mysql.connector.errors import ProgrammingError

user = 'root'
password = 'coderslab'
host = 'localhost'
database = 'twitter_db'

def testCreateUser():
    
    user1 = User()
    user1.name = 'frodo'
    user1.email = 'fb@ring.com'
    user1.set_password('precious')
    
    try:
        cnx = connect(user=user, password=password, host=host, database=database)
        print("Connected...")
        cursor = cnx.cursor()  
              
        user1.save_to_db(cursor)
        
        cnx.commit()           
        cursor.close()
        cnx.close()
        print('Disconnected...')
         
    except ProgrammingError:
            print("Not connected...")


if __name__ == "__main__":
    testCreateUser()