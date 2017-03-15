from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response
from mysql.connector import connect
from mysql.connector.errors import ProgrammingError
from models.tweet import *
from models.user import *
from models.comment import *
from models.crypto import *
from models.message import *
from datetime import datetime

def connect_db():
    user = 'root'
    password = 'coderslab'
    host = 'localhost'
    database = 'twitter_db'
    try:
        cnx = connect(user=user, password=password, host=host, database=database)
        print("Connected...")
        return cnx
        
    except ProgrammingError:
        print("Not connected...")

app = Flask(__name__)
 

@app.route('/login', methods=['GET', 'POST'])
def login():     
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cnx = connect_db()  
        cursor = cnx.cursor()
        sql = "SELECT user_id,hashed_password FROM Users WHERE email='{}'".format(username)
        result = cursor.execute(sql)
        data = cursor.fetchone()
        if data is None:
            error = 'Invalid username'
        elif not check_password(password, data[1]):
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['user_id'] = data[0]
#             flash('You were logged in')
            return redirect(url_for('all_tweets'))
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():     
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        
        cnx = connect_db()  
        cursor = cnx.cursor()
        sql = "SELECT user_id,hashed_password FROM Users WHERE email='{}'".format(email)
        result = cursor.execute(sql)
        data = cursor.fetchone()
        if data is None:
            if request.form['password1'] == request.form['password2']:
                password = request.form['password1']
                
                user = User()
                user.username = username
                user.email = email
                user.set_password(password,None)
                
                user.save_to_db(cursor)
                cnx.commit()
                
                session['logged_in'] = True
                session['user_id'] = cursor.lastrowid
                return redirect(url_for('all_tweets'))
            else:
                error='Different Passwords'
        else:
            error = 'User with this email already exist'
            
    return render_template('register.html', error=error)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    try:
        if not session['logged_in']:
           raise Exception
        
        cnx=connect_db()
        user = User.load_user_by_id(cnx.cursor(),session['user_id'])
        email = user.email     
        error = None
        if request.method == 'POST':
            username = request.form['username']
            
            if request.form['password1'] == request.form['password2']:
                password = request.form['password1']
                
                user.username = username
                user.set_password(password,None)
                user.save_to_db(cnx.cursor())
                cnx.commit()
                return redirect(url_for('all_tweets'))
            else:
                error='Different Passwords'
                
        return render_template('edit.html', error=error, email=email)
    except:
        return redirect(url_for('login'))

@app.route("/all_tweets", methods=['GET','POST'])
def all_tweets():
    try:
        if not session['logged_in']:
           raise Exception  
        if request.method == "GET":
            cnx = connect_db()  
            tweets=Tweet.load_all_tweets(cnx.cursor())
            html = '''
            <a href="http://127.0.0.1:5000/all_tweets" type="button" style="color:black" class="btn btn-default">All Tweets</a><br>
            <a href="http://127.0.0.1:5000/messages" type="button" style="color:black" class="btn btn-default">Messages</a>
            
            
                    <table style="width:50%; margin-left:auto; margin-right:auto;">
                      <tr>
                      <td colspan = "3">
                          <form method = 'POST'>
                             <div class="form-group">
                              <label for="new_tweet"><h3>New Tweet:</h3></label>
                              <textarea class="form-control" rows="5" name="new_tweet" style="width:100%"></textarea>
                              <input type="submit" value="Tweet">
                             </div>
                          </form>
                      </td>
                      </tr>
                      <tr>
                        <th align="left"><h3>All Tweets:</h3></th>
                      </tr>
                      <tr><td colspan="3"><hr></td></tr>
                      <tr>
                        <th align="left">Tweet Text</th>
                        <th align="right">Author</th>
                        <th align="right">Date Added</th>
                      </tr>
                      <tr><td colspan="3"><hr></td></tr>'''   
            for tweet in tweets:
                user = User.load_user_by_id(cnx.cursor(),tweet.user_id)
                html +='''
                        <tr>
                            <td><a href="http://127.0.0.1:5000/tweet_by_id/{}" style="color: black;text-decoration:none">{}</a></td>
                            <td align="right"><a href="http://127.0.0.1:5000/tweets_by_user_id/{}" style="color: black;text-decoration:none">{}</a></td>
                            <td align="right">{}</td>
                          </tr>'''.format(tweet.id,tweet.text,user.id,user.email,datetime.date(tweet.creation_date))
                
            html += '</table>'
            return html
      
        elif request.method == "POST":
            tweet = Tweet()
            tweet.user_id = session['user_id']
            tweet.text = request.form['new_tweet']
            tweet.creation_date = datetime.now()
            
            cnx = connect_db()
            tweet.add_tweet(cnx.cursor())
            cnx.commit()
            
            return redirect(url_for('all_tweets'))
    except:
        return redirect(url_for('login'))
    
@app.route("/tweets_by_user_id/<user_id>", methods=['GET','POST'])
def tweets_by_user_id(user_id): 
    try:
        if not session['logged_in']:
           raise Exception
           
        if request.method == "GET":
            cnx = connect_db()  
            tweets=Tweet.load_tweets_by_user_id(cnx.cursor(),user_id)
            user = User.load_user_by_id(cnx.cursor(),user_id)
            html = '''
                    <a href="http://127.0.0.1:5000/all_tweets" type="button" style="color:black" class="btn btn-default">All Tweets</a><br>
                    <a href="http://127.0.0.1:5000/messages" type="button" style="color:black" class="btn btn-default">Messages</a>
            
            
                    <table style="width:50%; margin-left:auto; margin-right:auto;">
                      <tr>
                            <th align="left"><h3>All Tweets by {}:</h3></th>
                            <th align="right">
                             <a href="http://127.0.0.1:5000/edit" type="button" style="color:black" class="btn btn-default">Edit User</a>
                            </th>
                            <th align="right">
                             <button type="button" class="btn btn-default">Send Message</button>
                            </th>
                          </tr>
                          <tr><td colspan="3"><hr></td></tr>
                          <tr>
                            <th align="left">Tweet Text</th>
                            <th align="right">Comments</th>
                            <th align="right">Date Added</th>
                          </tr>
                          <tr><td colspan="3"><hr></td></tr>'''.format(user.email)   
            for tweet in tweets:
                comments = Comment.load_comments_by_tweet_id(cnx.cursor(),tweet.id)
                html +='''
                        <tr>
                            <td><a href="http://127.0.0.1:5000/tweet_by_id/{}" style="color: black;text-decoration:none">{}</a></td>
                            <td align="right">{}</td>
                            <td align="right">{}</td>
                          </tr>'''.format(tweet.id,tweet.text,len(comments),datetime.date(tweet.creation_date))
                 
            html += '</table>'
        return html
    except:
            return redirect(url_for('login'))
   
@app.route("/tweet_by_id/<id>", methods=['GET','POST'])
def tweet_by_id(id):
    try:
        if not session['logged_in']:
           raise Exception 
    
        if request.method == "GET":
            cnx = connect_db()  
            tweet = Tweet.load_tweet_by_id(cnx.cursor(),id)
            user = User.load_user_by_id(cnx.cursor(),tweet.user_id)
            comments = Comment.load_comments_by_tweet_id(cnx.cursor(),id) 
            html ='''
                    <a href="http://127.0.0.1:5000/all_tweets" type="button" style="color:black" class="btn btn-default">All Tweets</a><br>
                    <a href="http://127.0.0.1:5000/messages" type="button" style="color:black" class="btn btn-default">Messages</a>
            
                    <table style="width:50%; margin-left:auto; margin-right:auto;">
                      <tr>
                         <th align="left"><h3>Id</h3></th>
                         <th align="left"><h3>Text</h3></th>
                         <th align="right"><h3>Author</h3></th>
                         <th align="right"><h3>Creation Date</h3></th>
                      </tr>
                      <tr><td colspan="4"><hr></td></tr>
                      <tr>
                        <th align="left">{}</th>
                        <th align="left">{}</th>
                        <th align="right"><a href="http://127.0.0.1:5000/tweets_by_user_id/{}" style="color: black;text-decoration:none">{}</a></th>
                        <th align="right">{} {}</th>
                      </tr>
                      <tr><td colspan="4"><hr></td></tr>
                      '''.format(tweet.id,tweet.text,user.id,user.email, datetime.date(tweet.creation_date),datetime.time(tweet.creation_date)) 
            html +='''
                    <table style="width:50%; margin-left:auto; margin-right:auto;">
                              <tr>
                                 
                              </tr>
                              <tr>
                                 <th align="left"><h4>Comments</h4></th>
                                 <th align="right"><h4>Author</h4></th>
                                 <th align="right"><h4>Creation Date</h4></th>
                              </tr>
                              <tr><td colspan="4"><hr></td></tr>
                              
                              
            '''
            for comment in comments:
                user_com = User.load_user_by_id(cnx.cursor(),comment.user_id)
                html +='''
                        <tr>
                            <td align="left">{}</td>
                            <td align="right"><a href="http://127.0.0.1:5000/tweets_by_user_id/{}" style="color: black;text-decoration:none">{}</a></td>
                            <td align="right">{}</td>
                          </tr>
                          '''.format(comment.text,user_com.id,user_com.email,datetime.date(comment.creation_date))
                
            
            html += '''<tr><td colspan="4"><hr></td></tr>
                    <tr>
                      <td colspan = "4">
                          <form method = 'POST'>
                             <div class="form-group">
                              <label for="new_comment"><h3>New Comment:</h3></label>
                              <textarea class="form-control" rows="5" name="new_comment" style="width:100%"></textarea>
                              <input type="submit" value="Comment">
                             </div>
                          </form>
                      </td>
                    </tr>
            '''
            return html
        elif request.method == "POST":
                comment = Comment()
                comment.user_id = session['user_id']
                comment.tweet_id = id
                comment.text = request.form['new_comment']
                comment.creation_date = datetime.now()
                
                cnx = connect_db()
                comment.add_comment(cnx.cursor())
                cnx.commit()
                return redirect(('tweet_by_id/{}'.format(id)))
    except:
            return redirect(url_for('login'))
        
@app.route("/messages", methods=['GET','POST'])
def messages():
#     try:
#         if not session['logged_in']:
#            raise Exception 
    
        if request.method == "GET":
            cnx = connect_db()  
            received = Message.load_messages_by_recipient_id(cnx.cursor(),session['user_id'])
            sent = Message.load_messages_by_sender_id(cnx.cursor(),session['user_id'])
            html ='''
                    <a href="http://127.0.0.1:5000/all_tweets" type="button" style="color:black" class="btn btn-default">All Tweets</a><br>
                    <a href="http://127.0.0.1:5000/messages" type="button" style="color:black" class="btn btn-default">Messages</a>
            
                    <table style="width:50%; margin-left:auto; margin-right:auto;">
                      <tr>
                        <th align="left"><h3>Received:</h3></th>
                      <tr>
                      <tr>
                         <th align="left"><h3>From</h3></th>
                         <th align="left"><h3>Text</h3></th>
                         <th align="right"><h3>Status</h3></th>
                         <th align="right"><h3>Date</h3></th>
                      </tr>
                      <tr><td colspan="4"><hr></td></tr>
                      '''
           
            for message in received:
                user = User.load_user_by_id(cnx.cursor(),message.sender_id)
                html +='''
                        <tr>
                        <td align="left">{}</td>
                        <td align="left">{}</td>
                        <td align="right">{}</td>
                        <td align="right">{}</td>
                      </tr>
                          '''.format(user.email,message.text, message.status,datetime.date(message.creation_date))
            html +='''
                    
                    <table style="width:50%; margin-left:auto; margin-right:auto;">
                      <tr>
                        <th align="left"><h3>Sent:</h3></th>
                      <tr>
                      <tr>
                         <th align="left"><h3>To</h3></th>
                         <th align="left"><h3>Text</h3></th>
                         <th align="right"><h3>Status</h3></th>
                         <th align="right"><h3>Date</h3></th>
                      </tr>
                      <tr><td colspan="4"><hr></td></tr>
                      '''
           
            for message in sent:
                user = User.load_user_by_id(cnx.cursor(),message.recipient_id)
                html +='''
                        <tr>
                        <td align="left">{}</td>
                        <td align="left">{}</td>
                        <td align="right">{}</td>
                        <td align="right">{}</td>
                      </tr>
                          '''.format(user.email,message.text, message.status,datetime.date(message.creation_date))              
                
            
            html += '''<tr><td colspan="4"><hr></td></tr>
                    <tr>
                      <td colspan = "4">
                          <form method = 'POST'>
                             <div class="form-group">
                              <input type="text" class="form-control" name="recipient_id" placeholder="Recipient ID" required="" autofocus="" >
                              <label for="new_message"><h3>New Message:</h3></label>
                              <textarea class="form-control" rows="5" name="new_message" style="width:100%"></textarea>
                              <input type="submit" value="Send">
                             </div>
                          </form>
                      </td>
                    </tr>
            '''
            return html
        elif request.method == "POST":
                message = Message()
                message.sender_id = session['user_id']
                message.recipient_id = int(request.form['recipient_id'])
                message.text = request.form['new_message']
                message.status = 0
                message.creation_date = datetime.now()
                
                cnx = connect_db()
                message.send_message(cnx.cursor())
                cnx.commit()
                return redirect(('messages'))
#     except:
#             return redirect(url_for('login'))
        


# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
  


if __name__ == "__main__":
    app.run()
    