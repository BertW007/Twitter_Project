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
        
    @staticmethod
    def load_comments_by_tweet_id(cursor, tweet_id):
        sql = """SELECT Comments.id, Comments.text, Comments.creation_date, Users.user_id, Users.email
                 FROM Comments
                 JOIN Users ON Comments.user_id=Users.user_id
                 WHERE Comments.tweet_id = {}
                 ORDER BY -Comments.creation_date;""".format(tweet_id)
        print(sql)
        ret = []
        result = cursor.execute(sql)
        data = cursor.fetchall()

        for row in data:
            loaded_comment = Comment()
            loaded_comment.__id = row[0]
            loaded_comment.text = row[1]
            loaded_comment.creation_date = row[2]
            loaded_comment.user_id = row[3]
            loaded_comment.email = row[4]
            ret.append(loaded_comment)
        return ret

    def add_comment(self, cursor):
        if self.__id == -1:
            sql_guery = """INSERT INTO Comments(user_id,tweet_id,text,creation_date) 
                        VALUES('{}','{}','{}','{}');
                        """.format(self.user_id, self.tweet_id, self.text, self.creation_date)
                
            cursor.execute(sql_guery)
            self.__id = cursor.lastrowid
            return True
#         else:
#             sql = "UPDATE Tweets SET text='{}',creation_date='{}' WHERE tweet_id={};".format(self.text, self.creation_date,  self.__id)
#             print(sql)
#             cursor.execute(sql)
#             return True TODO: new feature updating tweets
