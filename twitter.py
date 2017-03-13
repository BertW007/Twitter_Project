from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response
from mysql.connector import connect
from mysql.connector.errors import ProgrammingError
from models.tweet import *
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
 

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('twitter'))
#     return render_template('login.html', error=error)

@app.route("/all_tweets", methods=['GET','POST'])
def all_tweets(): 
    html = '<h3>All Twits:</h3>'
    
    if request.method == "GET":
        cnx = connect_db()  
        tweets=Tweet.load_all_tweets(cnx.cursor())
        html += '''
                <table style="width:50%">
                  <tr>
                    <th align="left">Tweet Text</th>
                    <th align="right">Date Added</th>
                  </tr>'''   
        for tweet in tweets:
            html +='''
                    <tr>
                        <td>{}</td>
                        <td align="right">{}</td>
                      </tr>'''.format(tweet.text,datetime.date(tweet.creation_date))
            
        html += '</table>'
        return html
  
    elif request.method == "POST":
        return 'POST'
    
@app.route("/tweets_by_user_id/<user_id>", methods=['GET','POST'])
def tweets_by_user_id(user_id): 
    html = '<h3>User id= {} Twits:</h3>'.format(user_id)
    
    if request.method == "GET":
        cnx = connect_db()  
        tweets=Tweet.load_tweets_by_user_id(cnx.cursor(),user_id)
        html += '''
                <table style="width:50%">
                  <tr>
                    <th align="left">Tweet Text</th>
                    <th align="right">Date Added</th>
                  </tr>'''   
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
    html = '<h3>Twitt id={}:</h3>'.format(id)
    
    if request.method == "GET":
        cnx = connect_db()  
        tweet=Tweet.load_tweet_by_id(cnx.cursor(),id)
        html +='{} {} {}'.format(tweet.text,datetime.date(tweet.creation_date),datetime.time(tweet.creation_date))   
    return html
  


if __name__ == "__main__":
    app.run()
    