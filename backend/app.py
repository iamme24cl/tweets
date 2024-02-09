from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import re

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tweets.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "myawesomesecretkeyhahahahaha"
CORS(app)
JWTManager(app)

# DB
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column('id', db.Integer, primary_key = True) 
    username = db.Column(db.String(24))
    email = db.Column(db.String(64))
    pwd = db.Column(db.String(64))

    # Constructor
    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd = pwd

def getUsers():
    users = User.query.all()
    return [{"id": u.id, "username": u.username, "email": u.email, "pwd": u.pwd} for u in users]

def getUser(uid):
    user = User.query.get(uid)
    return {"id": user.id, "username": user.username, "email": user.email, "pwd": user.pwd}

def addUser(username, email, pwd):
    try:
        user = User(username, email, pwd)
        db.session.add(user)
        db.session.commit()
        return jsonify({"success": "true"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Something went wrong!"}), 500
    
def removeUser(uid):
    uid = request.json["id"]        
    if uid:
        try:
            user = User.query.get(uid)
            db.session.delete(user)
            db.session.commit()
            return jsonify({"success": "true"}), 200
        except Exception as e:
            print(e)
            return jsonify({"error": "Something went wrong!"}), 500
    else:
        return jsonify({"error": "Invalid parameters"}), 400
    
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', foreign_keys=uid)
    title = db.Column(db.String(256))
    content = db.Column(db.String(2048))

    # constructor
    def __init__(self, title, content, userId):
        self.title = title
        self.content = content
        self.uid = userId

def getTweets():
    tweets = Tweet.query.all()
    return [{"id": t.id, "title": t.title, "content": t.content, "user": getUser(t.uid)} for t in tweets]

def getUserTweets(uid):
    tweets = Tweet.query.all()
    return [{"id": tweet.id, "uid": tweet.uid, "title": tweet.title, "content": tweet.content} for tweet in filter(lambda t: t.uid == uid, tweets)]

def addTweet(title, content, uid):
    try:
        user = list(filter(lambda u: u.id == uid, User.query.all()))[0]
        tweet = Tweet(title, content, user.id)
        db.session.add(tweet)
        db.session.commit()
        return jsonify({"success": "true"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Something went wrong!"}), 500
  
def delTweet(id):
    try:
        tweet = Tweet.query.get(id)
        db.session.delete(tweet)
        db.session.commit()
        return jsonify({"success": "true"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Something went wrong!"}), 500
  

# Routes
@app.route("/login", methods=["POST"])
def login():
    try:
        email = request.json["email"]
        pwd = request.json["pwd"]
        print(email)
        print(pwd) 
        print(getUsers())
        if email and pwd:
            user = list(filter(lambda u: u["email"] == email and u["pwd"] == pwd, getUsers()))
            print(user)
            print(len(user))
            if len(user) == 1:
                token = create_access_token(identity=user[0]["id"])
                return jsonify({"success": True, "token": token}), 200
            else:
                return jsonify({"error": "Unauthorized user!"}), 401
        else:
            return jsonify({"error": "Invalid Parameters"}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "Something went wrong!"}), 500
    

@app.route("/register", methods=["POST"])           
def register():
    try:
        email = request.json["email"].lower()
        pwd = request.json["pwd"]
        username = request.json["username"]
        # check to see if user already exists
        user = list(filter(lambda u: u["email"] == email and u["pwd"] == pwd, getUsers()))
        if len(user) == 1:
            return jsonify({"success": False, "error": "User with email " + user.email + " already exists!"}), 400
        # Email validation check
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
            return jsonify({"success": False, "error": "Invalid email"}), 400
        if email and pwd and username:  
            return addUser(username, email, pwd)
        else:
            return jsonify({"error": "Invalid parameters"}), 400
    except Exception as e:
        print("line 144")
        print(e)
        return jsonify({"error": "Something went wrong!"}), 500
    
@app.route("/tweets", methods=["GET", "POST", "DELETE"])
@jwt_required()
def tweets():
    method = request.method
    if method.lower() == "get": 
        return jsonify(getTweets()), 200
    elif method.lower() == "post":
        try:
            title = request.json["title"]
            content = request.json["content"]
            uid = request.json["uid"]
            if title and content and uid:
                return addTweet(title, content, uid)
            else:
                return jsonify({"error": "Invalid parameters"}), 400
        except Exception as e:
            print(e)
            return jsonify({"error": "Something went wrong!"}), 500
    elif method.lower() == "delete":
        try: 
            tweet_id = request.json["tid"]
            if tweet_id:
                return delTweet(tweet_id)
            else:
                return jsonify({"error": "Invalid parameters"}), 400
        except Exception as e:
            print(e)
            return jsonify({"error": "Something went wrong!"}), 500


@app.route('/users', methods=["GET", "POST", "DELETE"])
def users():
    method = request.method
    if method.lower() == "get": 
        users = User.query.all()
        return jsonify([{"id": user.id, "username": user.username, "email": user.email, "pwd": user.pwd} for user in users])
    elif method.lower() == "post":
        try:
            username = request.json["username"]
            email = request.json["email"]
            pwd = request.json["pwd"]
            if username and pwd and email:
                try:
                    user = User(username, email, pwd) 
                    db.session.add(user) # adds the record for committing
                    db.session.commit() # Saves our changes
                    return jsonify({"success": True}), 201
                except Exception as e:
                   print(e)
                   return jsonify({"error": "Something went wrong!"}), 500
            else:
                return jsonify({"error": "Invalid parameters"}), 400
        except Exception as e:
            print(e)
            return jsonify({"error": "Something went wrong!"}), 500
    elif method.lower() == "delete":
        try:
            uid = request.json["id"]
            if uid:
                try:
                    user = User.query.get(uid)
                    db.session.delete(user)
                    db.session.commit()
                    return jsonify({"success": True}), 201
                except Exception as e:
                    print(e)
                    return jsonify({"error": "Something went wrong!"}), 500
            else:
                return jsonify({"error": "Invalid Parameters"}), 400
        except Exception as e:
            print(e)
            return jsonify({"error": "Something went wrong!"}), 500

@app.route('/')
def root():
    db.create_all()
    return jsonify({"success": True, "message": "Hello from Tweets server!"}), 200

if __name__ == "__main__":
    app.run(debug=True) 

