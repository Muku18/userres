# Importing Modules
from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from werkzeug.security import generate_password_hash


# Initializing and Connecting to Database
app = Flask(__name__)
app.secret_key = "secretkey"
app.config['MONGO_URI'] =  "mongodb://localhost:27017/Users"
mongo = PyMongo(app)

# Creates a new user with the specified data.
@app.route('/users',methods = ['POST'])
def create_user():
    json = request.json
    _name = json['name']
    _email = json['email']
    _pass = json['pwd']
    if _name and _email and _pass and request.method == 'POST':
        hashed_pwd = generate_password_hash(_pass)
        id = mongo.db.user.insert_one({'name':_name,'email':_email,'pwd':hashed_pwd})
        res = jsonify("User added Successfully")
        res.status_code = 200
        return res
    else:
        return details_not_found()

# Returns a list of all users.
@app.route('/users',methods = ['GET'])
def displayusers():
    users = mongo.db.user.find()
    res = dumps(users)
    return res

# Returns the user with the specified ID.
@app.route('/users/<id>',methods = ['GET'])
def specificuser(id):
    user = mongo.db.user.find_one({'_id':ObjectId(id)})
    res = dumps(user)
    return res


# Updates the user with the specified ID with the new data.
@app.route('/users/<id>',methods = ['PUT'])
def updatespecificuser(id):
    _id = id
    json = request.json
    _name = json['name']
    _email = json['email']
    _pass = json['pwd']
    if _name and _email and _pass and _id and request.method == 'PUT':
        hashed_pwd = generate_password_hash(_pass)
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                 {'$set':{'name':_name,'email':_email,'pwd':hashed_pwd}})
        res = jsonify("User updated Successfully")
        res.status_code = 200
        return res
    else:
        return details_not_found()

# Deletes the user with the specified ID.
@app.route('/users/<id>',methods = ['DELETE'])
def deletespecificuser(id):
    mongo.db.user.delete_one({'_id':ObjectId(id)})
    res = jsonify("User deleted Successfully")
    res.status_code = 200
    return res



# Error handler function
@app.errorhandler(404)
def details_not_found(error = None):
    message = {
        'status' : 404,
        'message' : 'Details Not Found' + request.url
    }
    res = jsonify(message)
    res.status_code = 200
    return res


if __name__ == "__main__":
    app.run(debug = True)

