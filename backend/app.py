import re
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tweets.db"

# DB
db = SQLAlchemy(app)
class Users(db.Model):
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
    users = Users.query.all()
    return [{"id": u.id, "username": u.username, "email": u.email, "pwd": u.pwd} for u in users]

def addUser(username, email, pwd):
    if username and email and pwd:
        try:
            user = Users(username, email, pwd)
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False 
    else:
        return False 

def removeUser(uid):
    uid = request.json["id"]        
    if uid:
        try:
            user = Users.query.get(uid)
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False


# Routes
@app.route("/login", methods=["POST"])
def login():
    try:
        email = request.json["email"]
        pwd = request.json["pwd"]
        if email and pwd:
            users = getUsers()
            for user in users:
                if user["email"] == email and user["pwd"] == pwd:
                    return jsonify({"status": 200, "success": True})
                else:
                    return jsonify({"status": 404, "message": "User not found!"})
        else:
            return jsonify({"status": 404, "error": "Invalid Parameters"})
    except Exception as e:
        print(e)
        return jsonify({"status": 500, "error": "Something went wrong!"})
    

@app.route("/register", methods=["POST"])           
def register():
    try:
        email = request.json["email"].lower()
        pwd = request.json["pwd"]
        username = request.json["username"]
        # check to see if user already exists
        users = getUsers()
        for user in users:
            if user["email"] == email and user["pwd"] == pwd:
                return jsonify({"status": 404, "success": False, "message": "User with email " + user.email + " already exists!"})
        # Email validation check
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
            return jsonify({"status": 404, "success": False, "message": "Invalid email"})
        
        addUser(username, email, pwd)
        return jsonify({"status": 201, "success": True})
    except:
        return jsonify({"status": 500, "error": "Something went wrong!"})


@app.route('/users', methods=["GET", "POST", "DELETE"])
def users():
    method = request.method
    if method.lower() == "get": 
        users = Users.query.all()
        return jsonify([{"id": user.id, "username": user.username, "email": user.email, "pwd": user.pwd} for user in users])
    elif method.lower() == "post":
        try:
            username = request.json["username"]
            email = request.json["email"]
            pwd = request.json["pwd"]
            if username and pwd and email:
                try:
                    user = Users(username, email, pwd) 
                    db.session.add(user) # adds the record for committing
                    db.session.commit() # Saves our changes
                    return jsonify({"success": True})
                except Exception as e:
                    return ({"error": e})
            else:
                return jsonify({"error": "Invalid parameters"})
        except:
            return jsonify({"error": "Invalid Parameters"})
    elif method.lower() == "delete":
        try:
            uid = request.json["id"]
            if uid:
                try:
                    user = Users.query.get(uid)
                    db.session.delete(user)
                    db.session.commit()
                    return jsonify({"success": True})
                except Exception as e:
                    return ({"error": e})
            else:
                return jsonify({"error": "Invalid Parameters"})
        except:
            return jsonify({"error": "Invalid Parameters"})


if __name__ == "__main__":
    app.run(debug=True) 

