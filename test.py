from models.users import User
from mysql.connector import connect
from mysql.connector.errors import ProgrammingError

user = 'root'
password = 'coderslab'
host = 'localhost'
database = 'twitter_db'

def testCreateUser():
    
    try:
        cnx = connect(user=user, password=password, host=host, database=database)
        print("Connected...")
#         cursor = cnx.cursor()  
#              
#         query = 'INSERT INTO Cinemas (name,adress) VALUES ("{}","{}")'.format(options.name,options.adress)
#         print(query)
#         try:
#             cursor.execute(query)
#             cnx.commit()
#             print('Do bazy danych Cinemas dodano kino o id={}'.format(cursor.lastrowid))       
#         except (DatabaseError, ProgrammingError):
#             print('Nie udało się dodać kina')
#                   
#         cursor.close()
#         cnx.close()
        print('Disconnected...')
         
    except ProgrammingError:
            print("Not connected...")


if __name__ == "__main__":
    testCreateUser()