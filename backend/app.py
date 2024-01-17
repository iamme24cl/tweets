from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tweets.db"

# DB
db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column('id', db.Integer, primary_key = True) # primary_key makes it so that this value is unique and can be used to identify this record.
    username = db.Column(db.String(24))
    email = db.Column(db.String(64))
    pwd = db.Column(db.String(64))

    # Constructor
    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.pwd = pwd

# Routes
@app.route('/users', methods=["GET", "POST", "DELETE"])
def users():
    method = request.method
    if method.lower() == "get": 
        users = Users.query.all()
        return jsonify([{"id": user.id, "username": user.username, "email": user.email, "password": user.pwd} for user in users])
    elif method.lower() == "post":
        try:
            username = request.json["username"]
            email = request.json["email"]
            pwd = request.json["pwd"]
            if username and pwd and email:
                try:
                    user = Users(username, email, pwd) # Creates new record
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
    app.run(debug=True) # debug=True restarts the server everytime we make a change in our code