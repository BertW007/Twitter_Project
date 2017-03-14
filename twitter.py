from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response
from mysql.connector import connect
from mysql.connector.errors import ProgrammingError
from models.tweet import *
from models.user import *
from models.crypto import *
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
        print(sql)
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

@app.route("/all_tweets", methods=['GET','POST'])
def all_tweets():
    try:
        if not session['logged_in']:
           raise Exception  
        if request.method == "GET":
            cnx = connect_db()  
            tweets=Tweet.load_all_tweets(cnx.cursor())
            html = '''
                    <table style="width:50%; margin-left:auto; margin-right:auto;">
                      <tr>
                      <td colspan = "3">
                          <form method = 'POST'>
                             <div class="form-group">
                              <label for="new_tweet"><h3>New Tweet:</h3></label>
                              <textarea class="form-control" rows="5" name="new_tweet" style="width:100%"></textarea>
                              <input type="submit" value="Submit">
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
                            <td>{}</td>
                            <td align="right">{}</td>
                            <td align="right">{}</td>
                          </tr>'''.format(tweet.text,user.email,datetime.date(tweet.creation_date))
                
            html += '</table>'
            return html
      
        elif request.method == "POST":
            tweet = Tweet()
            tweet.user_id = session['user_id']
            tweet.text = request.form['new_tweet']
            tweet.creation_date = datetime.now()
            
            cnx = connect_db()
            tweet.add_edit_tweet(cnx.cursor())
            cnx.commit()
            
            return redirect(url_for('all_tweets'))
    except:
        return redirect(url_for('login'))
    
@app.route("/tweets_by_user_id/<user_id>", methods=['GET','POST'])
def tweets_by_user_id(user_id):   
    if request.method == "GET":
        cnx = connect_db()  
        tweets=Tweet.load_tweets_by_user_id(cnx.cursor(),user_id)
        user = User.load_user_by_id(cnx.cursor(),user_id)
        html = '''
                <table style="width:50%; margin-left:auto; margin-right:auto;">
                  <tr>
                        <th align="left"><h3>All Tweets by {}:</h3></th>
                      </tr>
                      <tr><td colspan="2"><hr></td></tr>
                      <tr>
                        <th align="left">Tweet Text</th>
                        <th align="right">Date Added</th>
                      </tr>
                      <tr><td colspan="2"><hr></td></tr>'''.format(user.email)   
        for tweet in tweets:
            html +='''
                    <tr>
                        <td>{}</td>
                        <td align="right">{}</td>
                      </tr>'''.format(tweet.text,datetime.date(tweet.creation_date))
             
        html += '</table>'
    return html
  

    
@app.route("/tweet_by_id/<id>", methods=['GET','POST'])
def tweet_by_id(id): 
    
    if request.method == "GET":
        cnx = connect_db()  
        tweet = Tweet.load_tweet_by_id(cnx.cursor(),id)
        user = User.load_user_by_id(cnx.cursor(),tweet.user_id) 
        html ='''
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
                    <th align="right">{}</th>
                    <th align="right">{} {}</th>
                  </tr>
                  <tr><td colspan="4"><hr></td></tr>
                  '''.format(tweet.id,tweet.text,user.email, datetime.date(tweet.creation_date),datetime.time(tweet.creation_date)) 
    return html

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
  


if __name__ == "__main__":
    app.run()
    