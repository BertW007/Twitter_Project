from datetime import datetime

class Comment(object):
    __id = None
    user_id = None
    tweet_id = None
    text = None
    creation_date = None
    
    def __init__(self):
        self.__id = -1
        self.user_id = 0
        self.tweet_id = 0
        self.text = ''
        self.creation_date = ''
        
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
    def load_comment_by_id(cursor, id):
        sql = "SELECT id, text, creation_date,user_id FROM Tweets WHERE id={}".format(id)
        result = cursor.execute(sql)
        data = cursor.fetchone()
         
        if data is not None:
            loaded_tweet = Tweet()
            loaded_tweet.__id = data[0]
            loaded_tweet.text = data[1]
            loaded_tweet.creation_date = data[2]
            loaded_tweet.user_id = data[3]
            return loaded_tweet
        else:
            return None
        
    @staticmethod
    def load_comments_by_tweet_id(cursor, user_id):
        sql = "SELECT Tweets.id, Tweets.text, Tweets.creation_date, Users.name FROM Tweets JOIN Users ON Tweets.user_id=Users.user_id WHERE Users.user_id ={} ORDER BY -creation_date;".format(user_id)
        print(sql)
        ret = []
        result = cursor.execute(sql)
        data = cursor.fetchall()

        for row in data:
            loaded_tweet = Tweet()
            loaded_tweet.__id = row[0]
            loaded_tweet.text = row[1]
            loaded_tweet.creation_date = row[2]
            ret.append(loaded_tweet)
        return ret
        
        
    def add_comment(self, cursor):
        if self.__id == -1:
            sql_guery = """INSERT INTO Comments(user_id,tweet_id,text,creation_date) 
                        VALUES('{}','{}','{}','{}');
                        """.format(self.user_id,self.tweet_id,self.text,self.creation_date)
                
            cursor.execute(sql_guery)
            self.__id = cursor.lastrowid
            return True
#         else:
#             sql = "UPDATE Tweets SET text='{}',creation_date='{}' WHERE tweet_id={};".format(self.text, self.creation_date,  self.__id)
#             print(sql)
#             cursor.execute(sql)
#             return True
        
    