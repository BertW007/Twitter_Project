# Twitter - Home Made
>*Project created as a part of Coders Lab boot camp in Warsaw.*

It is a home made Twitter with some simple functions.

## 1. Set Up
Set Up instruction

## 2. Models
Models are mapped into database.
### 2.1 Tweet
   Tweet model represents a single Tweet. It has four fields: id, author, text and creation date. One User can have many Tweets.
### 2.2 Comment
   Comment represents a single Comment. Like Tweet it has four fields  id, author, text and creation date. One Tweet can have many comments.
### 2.3 Message
   Message model represents a single Message. It has following fields: id, sender, recipient, title, text, status and creation date. One User can send and receive many Messages.
### 2.4 User
   User model represents an User. It has following fields: id, username, email, password.

## 3. Views
All Views can be divided into three categories as follows.
### 3.1 User
- /login/ - user login page
- /logout/ - user logout page
- /register/ - enables creating new user
- /edit/ - enables editing existing user

### 3.2 Tweet
- /all_tweets/ - showing all tweets
- /tweets_by_user_id/<user_id> - showing all tweets created by specified user
- /tweet_by_id/<tweet_id> - showing details e.g. comments, author etc. of a chosen tweet

### 3.3 Messages
- /messages/ - showing all messages, received and send by current user
- /message_by_id/<message_id> - showing details of a chosen message
- /new_message/ - enables creation and sending new message

## 4.Features
Features...

## 5.Tests
Tests created wit TDD philosophy.

@created by brzydal
