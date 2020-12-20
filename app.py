import json

from flask import Flask, request, Response
from pymongo import MongoClient, errors
from bson import json_util
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
mongo = MongoClient('mongo', 27017).demo
usersCollection = mongo.users

def getNextUserId():
    user_list = usersCollection.find().sort([("_id", -1)]).limit(1)
    users = list(user_list)
    app.logger.info('--------------- users = %s', users)
    if len(users) == 0: 
        return 1
    return users[0]['_id'] + 1

@app.route("/users", methods=["PUT"])
def add_user():
    """Create user
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
      - name: name
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Creation succeded
    """
    request_params = request.form
    if 'email' not in request_params or 'name' not in request_params:
        return Response('Email and name not present in parameters!', status=404, mimetype='application/json')
    try:
        userid = getNextUserId()
        usersCollection.insert_one({
            '_id': userid,
            'email': request_params['email'],
            'name': request_params['name']
        })
    except errors.DuplicateKeyError as e:
        return Response('Duplicate user id!', status=404, mimetype='application/json')
    return Response(json.dumps(usersCollection.find_one({'_id': userid})), status=200, mimetype='application/json')


@app.route("/users/<int:userid>", methods=["POST"])
def update_user(userid):
    """Update user information
    ---
    parameters:
      - name: userid
        in: path
        type: string
        required: true
      - name: email
        in: formData
        type: string
        required: false
      - name: name
        in: formData
        type: string
        required: false
    responses:
      200:
        description: Update succeded
    """
    request_params = request.form
    if 'email' not in request_params and 'name' not in request_params:
        return Response('Email or name must be present in parameters!', status=404, mimetype='application/json')
    set = {}
    if 'email' in request_params:
        set['email'] = request_params['email']
    if 'name' in request_params:
        set['name'] = request_params['name']
    usersCollection.update_one({'_id': userid}, {'$set': set})
    return Response(json.dumps(usersCollection.find_one({'_id': userid})), status=200, mimetype='application/json')


@app.route("/users/<int:userid>", methods=["GET"])
def get_user(userid):
    """Details about a user
    ---
    parameters:
      - name: userid
        in: path
        type: string
        required: true
    definitions:
      User:
        type: object
        properties:
          _id:
            type: integer
          email:
            type: string
          name:
            type: string
    responses:
      200:
        description: User model
        schema:
          $ref: '#/definitions/User'
      404:
        description: User not found
    """
    user = usersCollection.find_one({'_id': userid})
    app.logger.info('---------------%s ', user)
    if None == user:
        return Response("User was not found", status=404, mimetype='application/json')
    return Response(json.dumps(user), status=200, mimetype='application/json')


@app.route("/users", methods=["GET"])
def get_users():
    """Example endpoint returning all users with pagination
    ---
    parameters:
      - name: pageSize
        in: formData
        type: integer
        required: false
      - name: pageIndex
        in: formData
        type: integer
        required: false
    definitions:
      PageUsers:
        type: object
        properties:
          data:
            type: array
            items:
              properties:
                _id:
                  type: integer
                email:
                  type: string
                name:
                  type: string
          total:
            type: integer
          pageSize:
            type: integer
          pageIndex:
            type: integer
    responses:
      200:
        description: List of user models
        schema:
          $ref: '#/definitions/PageUsers'
    """
    request_params = request.form
    pageSize = int(request_params['pageSize']) if 'pageSize' in request_params else 10
    pageIndex = int(request_params['pageIndex']) if 'pageIndex' in request_params else 1
    user_list = usersCollection.find().limit(pageSize).skip(pageSize*(pageIndex-1))
    total = usersCollection.count_documents({})
    extracted = {
        'data': [
            {'userid': d['_id'],
            'name': d['name'],
            'email': d['email']
            } for d in user_list],
        'total': total,
        'pageSize': pageSize,
        'pageIndex': pageIndex,
        'success': True
    }
    return Response(json.dumps(extracted, default=json_util.default), status=200, mimetype='application/json')


@app.route("/users/<int:userid>", methods=["DELETE"])
def delete_user(userid):
    """Delete operation for a user
    ---
    parameters:
      - name: userid
        in: path
        type: string
        required: true
    responses:
      200:
        description: User deleted
    """
    usersCollection.delete_one({'_id': userid})
    return Response('', status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)