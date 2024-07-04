from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash
import os

app = Flask(__name__)
app.secret_key = "secretkey"

app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongodb:27017/userDetails")
mongo = PyMongo(app)

@app.route('/')
def index():
    return "Welcome to the Flask API"

@app.route('/add',methods = ['POST'])
def add_user_details():
    _json = request.json
    _userid = _json['userid']
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _userid and _name and _email and _password and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)
        id = mongo.db.details.insert_one({'userid' : _userid ,'name': _name , 'email': _email, 'password': _hashed_password})
        resp = jsonify("User added successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/userlist')
def userlist():
    userlist = mongo.db.details.find()
    resp = dumps(userlist)
    return resp

@app.route('/userlistone/<id>')
def userlistone(id):
    userlistone = mongo.db.details.find_one({'_id': ObjectId(id)})
    resp = dumps(userlistone)
    return resp

@app.route('/delete/<id>', methods =['DELETE'])
def delete(id):
    delete = mongo.db.details.delete_one({'_id': ObjectId(id)})
    resp = jsonify("User deleted Successfully")
    resp.status_code=200 
    return resp

@app.route('/update/<id>', methods =['PUT'])
def update(id):
    _id = id
    _json = request.json
    _userid = _json['userid']
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _id and _userid and _name and _email and _password and request.method == 'PUT':
        _hashed_password = generate_password_hash(_password)
        mongo.db.details.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': 
                {'userid' : _userid ,
                 'name': _name ,
                 'email': _email, 
                 'password': _hashed_password
                 }
            })
        resp = jsonify("User updated successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()
    
@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code =404
    return resp
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

