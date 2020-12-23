from flask import Blueprint, request, Response
from pymongo import errors
from bson import json_util
from flasgger import swag_from
from ...db import db
from ...models.user import User
from ...utils.auth import generateToken

api = Blueprint("auth", __name__, url_prefix="/api")


@api.route("/login", methods=["POST"])
@swag_from("docs/login.yml")
def login():
    data = request.get_json()
    if "username" not in data or "password" not in data:
        return Response(
            "Username and password not present in parameters!",
            status=404,
            mimetype="application/json",
        )
    username = data["username"]
    password = data["password"]
    user = User({"username": username, "password": password})
    result = user.checkExist()
    if not result:
        message = {"message": "Tài khoản không tồn tại"}
    token = generateToken({"id": result})
    message = {"token": token}
    return Response(
        json_util.dumps(message, default=json_util.default),
        status=200,
        mimetype="application/json",
    )
