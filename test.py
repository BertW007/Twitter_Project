from models.user import User
from models.tweet import Tweet
from mysql.connector import connect
from mysql.connector.errors import ProgrammingError
from datetime import datetime

user = 'root'
password = 'coderslab'
host = 'localhost'
database = 'twitter_db'

def connect_db(user,password,host,database):
    try:
        cnx = connect(user=user, password=password, host=host, database=database)
        cursor = cnx.cursor()
        print("Connected...")
    except ProgrammingError:
        print("Not connected...") 

def disconnect():
    cnx.commit()           
    cursor.close()
    cnx.close()
    print('Disconnected...')
    

def testCreateUser():
    new_user = User()
    new_user.name = 'sam'
    new_user.email = 'sam@gamgee.com'
    new_user.set_password('sam',None)
    
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
            
def testModifyUser():
    
    try:
        cnx = connect(user=user, password=password, host=host, database=database)
        print("Connected...")
        cursor = cnx.cursor()  
        try:      
            mod_user = User.load_user_by_id(cursor,5)
            print(mod_user.username, '-' , mod_user.email)
            mod_user.username = 'smeagol'
            mod_user.email = 'smeagol@ring.com'
            print(mod_user.username, '-' , mod_user.email)
            mod_user.save_to_db(cursor)
            
        except TypeError:
            print('There is no such record in database...')
            
        cnx.commit()           
        cursor.close()
        cnx.close()
        print('Disconnected...')
         
    except TypeError:
            print("Not connected...")
            
def testDeleteUser():
    
    try:
        cnx = connect(user=user, password=password, host=host, database=database)
        print("Connected...")
        cursor = cnx.cursor()  
        try:      
            del_user = User.load_user_by_id(cursor,5)
            del_user.delete(cursor)
            
        except TypeError:
            print('There is no such record in database...')
            
        cnx.commit()           
        cursor.close()
        cnx.close()
        print('Disconnected...')
         
    except TypeError:
            print("Not connected...")
            
def testCreateTweet():
    new_tweet = Tweet()
    new_tweet.text = 'gollsdfsdfsdfsfdsdfum'
    new_tweet.creation_date = datetime.now()
    print(new_tweet.id)
    
    try:
        cnx = connect(user=user, password=password, host=host, database=database)
        print("Connected...")
        cursor = cnx.cursor()  
              
        new_tweet.add_edit_tweet(cursor)
        
        cnx.commit()           
        cursor.close()
        cnx.close()
        print('Disconnected...')
         
    except ProgrammingError:
            print("Not connected...")
    
    


if __name__ == "__main__":
    testCreateUser()