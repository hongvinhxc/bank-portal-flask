from flask import Blueprint, request, Response
from pymongo import errors
from bson import json_util
from flasgger import swag_from
from ...db import db
from ...models.account import Account
from ...utils.auth import authMiddleware

api = Blueprint("accounts", __name__, url_prefix="/api")


@api.route("/accounts", methods=["GET"])
@authMiddleware
@swag_from("docs/get_accounts.yml")
def get_accounts():

    pageSize = int(request.args.get("pageSize")) if "pageSize" in request.args else 10
    pageIndex = int(request.args.get("pageIndex")) if "pageIndex" in request.args else 1
    keyword = request.args.get("keyword") if "keyword" in request.args else ''
    account_list = Account().getList(pageSize, pageIndex, keyword)
    data = list(account_list)
    totalData = data[0]['totalData'],
    totalCount = data[0]['totalCount']
    if not totalCount:
        total = 0
    else:
        total = totalCount[0]['count']
    extracted = {
        "data": totalData[0],
        "total": total,
        "pageSize": pageSize,
        "pageIndex": pageIndex,
        'keyword': keyword,
        "success": True,
    }
    return Response(
        json_util.dumps(extracted, default=json_util.default),
        status=200,
        mimetype="application/json",
    )


@api.route("/accounts", methods=["PUT"])
@authMiddleware
@swag_from("docs/add_account.yml")
def add_account():
    data = request.get_json()
    if "_id" in data:
        del data["_id"]
    if "firstname" not in data or "lastname" not in data:
        return Response(
            json_util.dumps(
                {"success": True, "message": "Name not present in parameters!"}
            ),
            status=404,
            mimetype="application/json",
        )
    account = Account(data)
    account.save()
    return Response(
        json_util.dumps(
            {"success": True, "message": "Add account successful!", "data": account}
        ),
        status=200,
        mimetype="application/json",
    )


@api.route("/accounts/<string:accountid>", methods=["POST"])
@authMiddleware
@swag_from("docs/update_account.yml")
def update_account(accountid):
    data = request.get_json()
    if "firstname" not in data or "lastname" not in data:
        return Response(
            json_util.dumps(
                {"success": False, "message": "Name not present in parameters!"}
            ),
            status=404,
            mimetype="application/json",
        )
    data["_id"] = accountid
    account = Account(data)
    account.save()
    return Response(
        json_util.dumps(
            {"success": True, "message": "Update account successful!", "data": account}
        ),
        status=200,
        mimetype="application/json",
    )


@api.route("/accounts/<string:accountid>", methods=["GET"])
@authMiddleware
@swag_from("docs/get_account.yml")
def get_account(accountid):
    account = Account({"_id": accountid})
    account.reload()
    if None == account:
        return Response(
            json_util.dumps({"success": False, "message": "Account was not found"}),
            status=404,
            mimetype="application/json",
        )
    return Response(json_util.dumps(account), status=200, mimetype="application/json")


@api.route("/accounts/<string:accountid>", methods=["DELETE"])
@authMiddleware
@swag_from("docs/delete_account.yml")
def delete_account(accountid):
    try:
        account = Account({"_id": accountid})
        account.remove()
    except:
        return Response(
            json_util.dumps({"success": False, "message": "Account is not exist"}),
            status=404,
            mimetype="application/json",
        )
    return Response(
        json_util.dumps(
            {
                "success": True,
                "message": "Delete account successful!",
                "deletedId": accountid,
            }
        ),
        status=200,
        mimetype="application/json",
    )
