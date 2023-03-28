from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.security import generate_password_hash

app = Flask(__name__)
api = Api(app)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['Users']
mongo = db['user']

# User resource fields
user_fields = {
    'id': fields.String(attribute='_id'),
    'name': fields.String,
    'email': fields.String,
    'password': fields.String,
}

# User resource parser
user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=str, required=True, help='Name is required')
user_parser.add_argument('email', type=str, required=True, help='Email is required')
user_parser.add_argument('password', type=str, required=True, help='Password is required')


class User(Resource):
    @marshal_with(user_fields)
    def get(self, user_id=None):
        if user_id is None:
            return list(mongo.find()), 200
        else:
            user = mongo.find_one({'_id': ObjectId(user_id)})
            return user, 200
    @marshal_with(user_fields)
    def post(self, ):
        # Create a new user
        args = user_parser.parse_args()
        _pass = args['password']
        hashed_pwd = generate_password_hash(_pass)
        user = {'name': args['name'], 'email': args['email'], 'password': hashed_pwd}
        user_id = mongo.insert_one(user)
        if user_id.acknowledged:
            return {'message': 'User created', 'id': str(user_id.inserted_id)}, 201
        else:
            return {'message': 'Error creating user'}, 500

    @marshal_with(user_fields)
    def put(self, user_id):
        # Update a user by id
        args = user_parser.parse_args()
        _pass = args['password']
        hashed_pwd = generate_password_hash(_pass)
        user = {'name': args['name'], 'email': args['email'], 'password': hashed_pwd}
        result = mongo.update_one({'_id': ObjectId(user_id)}, {'$set': user})
        if result.modified_count:
            return jsonify({'message': 'User updated'})
        else:
            return jsonify({'message': 'User not found'}), 404

    def delete(self, user_id):
        result = mongo.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count:
            return jsonify({'message': 'User deleted'})
        else:
            return jsonify({'message': 'User not found'}), 404


api.add_resource(User, '/users', '/users/<string:user_id>')
if __name__ == '__main__':
    app.run(debug=True)

