from datetime import datetime

class Message(object):
    __id = None
    sender_id = None
    recipient_id = None
    text = None
    status = None
    creation_date = None
    
    def __init__(self):
        self.__id = -1
        sender_id = 0
        recipient_id = 0
        text = ''
        status = False
        creation_date = datetime.now()
        
    @property
    def id(self):
        return self.__id
        
#     @staticmethod
#     def load_all_tweets(cursor):
#         sql = "SELECT id, text, creation_date,user_id FROM Tweets ORDER BY -creation_date"
#         ret = []
#         result = cursor.execute(sql)
#         data = cursor.fetchall()
# 
#         for row in data:
#             loaded_tweet = Tweet()
#             loaded_tweet.__id = row[0]
#             loaded_tweet.text = row[1]
#             loaded_tweet.creation_date = row[2]
#             loaded_tweet.user_id = row[3]
#             ret.append(loaded_tweet)
#         return ret
    
    @staticmethod
    def load_messages_by_sender_id(cursor,sender_id):
        sql = """SELECT id,recipient_id,text,status,creation_date
                FROM Messages WHERE id={}""".format(sender_id)
        result = cursor.execute(sql)
        data = cursor.fetchall()
        ret = []
         
        for row in data:
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.recipient_id = row[1]
            loaded_message.text = row[2]
            loaded_message.status = row[3]
            loaded_message.creation_date = row[4]
            ret.append(loaded_message)
        return ret
    
    @staticmethod
    def load_messages_by_recipient_id(cursor,recipient_id):
        sql = """SELECT id,sender_id,text,status,creation_date
                FROM Messages WHERE id={}""".format(recipient_id)
        result = cursor.execute(sql)
        data = cursor.fetchall()
        ret = []
         
        for row in data:
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.sender_id = row[1]
            loaded_message.text = row[2]
            loaded_message.status = row[3]
            loaded_message.creation_date = row[4]
            ret.append(loaded_message)
        return ret
    
    
        
#     @staticmethod
#     def load_messages_by_tweet_id(cursor, tweet_id):
#         sql = """SELECT messages.id, messages.user_id, messages.text, messages.creation_date 
#                 FROM messages JOIN Tweets ON messages.tweet_id=Tweets.id 
#                 WHERE messages.tweet_id ={} ORDER BY -messages.creation_date;""".format(tweet_id)
#         print(sql)
#         ret = []
#         result = cursor.execute(sql)
#         data = cursor.fetchall()
# 
#         for row in data:
#             loaded_message = message()
#             loaded_message.__id = row[0]
#             loaded_message.user_id = row[1]
#             loaded_message.text = row[2]
#             loaded_message.creation_date = row[3]
#             ret.append(loaded_message)
#         return ret
        
        
    def send_message(self, cursor):
        if self.__id == -1:
            sql_guery = """INSERT INTO Messages(sender_id,recipient_id,text,status,creation_date) 
                        VALUES('{}','{}','{}','{}','{}');
                        """.format(self.sender_id,self.recipient_id,self.text,self.status,self.creation_date)
                
            cursor.execute(sql_guery)
            self.__id = cursor.lastrowid
            return True
#         else:
#             sql = "UPDATE Tweets SET text='{}',creation_date='{}' WHERE tweet_id={};".format(self.text, self.creation_date,  self.__id)
#             print(sql)
#             cursor.execute(sql)
#             return True
        
    