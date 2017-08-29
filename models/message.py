from datetime import datetime


class Message(object):
    __id = None
    sender_id = None
    recipient_id = None
    title = None
    text = None
    status = None
    creation_date = None
    
    def __init__(self):
        self.__id = -1
        self.sender_id = 0
        self.recipient_id = 0
        self.title = ''
        self.text = ''
        self.status = False
        self.creation_date = datetime.now()
        
    @property
    def id(self):
        return self.__id

    @staticmethod
    def load_messages_by_sender_id(cursor, sender_id):
        sql = """SELECT id, recipient_id, title, text, status, creation_date, email
                 FROM Messages
                 JOIN Users ON Messages.recipient_id=Users.user_id
                 WHERE sender_id={}
                 ORDER BY -creation_date""".format(sender_id)
        print(sql)
        result = cursor.execute(sql)
        data = cursor.fetchall()
        ret = []
         
        for row in data:
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.recipient_id = row[1]
            loaded_message.title = row[2]
            loaded_message.text = row[3]
            loaded_message.status = row[4]
            loaded_message.creation_date = row[5]
            loaded_message.recipient_email = row[6]
            ret.append(loaded_message)
        return ret
    
    @staticmethod
    def load_messages_by_recipient_id(cursor, recipient_id):
        sql = """SELECT id, sender_id, title, text, status, creation_date, email
                 FROM Messages
                 JOIN Users ON Messages.sender_id=Users.user_id
                 WHERE recipient_id={}
                 ORDER BY -creation_date""".format(recipient_id)
        print(sql)
        result = cursor.execute(sql)
        data = cursor.fetchall()
        ret = []
         
        for row in data:
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.sender_id = row[1]
            loaded_message.title = row[2]
            loaded_message.text = row[3]
            loaded_message.status = row[4]
            loaded_message.creation_date = row[5]
            loaded_message.sender_email = row[6]
            ret.append(loaded_message)
        return ret
    
    @staticmethod
    def load_message_by_id(cursor,message_id):
        sql = """SELECT U1.email,U2.email,title,text,status,creation_date FROM Messages
                 JOIN Users U1 ON U1.user_id=Messages.sender_id
                 JOIN Users U2 ON U2.user_id=Messages.recipient_id
                 WHERE id={};""".format(message_id)
        print(sql)
        result = cursor.execute(sql)
        data = cursor.fetchone()
         
        if data is not None:
            loaded_message = Message()
            loaded_message.sender_email = data[0]
            loaded_message.recipient_email = data[1]
            loaded_message.title = data[2]
            loaded_message.text = data[3]
            loaded_message.status = data[4]
            loaded_message.creation_date = data[5]
            return loaded_message
        else:
            return None

    def send_message(self, cursor):
        if self.__id == -1:
            sql_guery = """INSERT INTO Messages(sender_id,recipient_id,title,text,status,creation_date) 
                        VALUES('{}','{}','{}','{}','{}','{}');
                        """.format(self.sender_id,
                                   self.recipient_id,
                                   self.title,
                                   self.text,
                                   self.status,
                                   self.creation_date)
                
            cursor.execute(sql_guery)
            self.__id = cursor.lastrowid
            return True
#         else:
#             sql = "UPDATE Tweets SET text='{}',creation_date='{}' WHERE tweet_id={};".format(self.text, self.creation_date,  self.__id)
#             print(sql)
#             cursor.execute(sql)
#             return True TODO: new feature updating messages
