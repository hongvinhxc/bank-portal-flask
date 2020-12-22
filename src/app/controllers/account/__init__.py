from flask import Blueprint, request, Response
from pymongo import errors
from bson import json_util
from flasgger import swag_from
from ...db import db
from ...models.account import Account
from ...utils.auth import authMiddleware

api = Blueprint('accounts', __name__, url_prefix='/api')

@api.route("/accounts", methods=["POST"])
@authMiddleware
@swag_from('docs/get_accounts.yml')
def get_accounts():
    
    request_params = request.form
    pageSize = int(request_params['pageSize']) if 'pageSize' in request_params else 10
    pageIndex = int(request_params['pageIndex']) if 'pageIndex' in request_params else 1
    account_list = Account().getList(pageSize, pageIndex)
    total = Account().count()
    data = list(account_list)
    extracted = {
        'data': data,
        'total': total,
        'pageSize': pageSize,
        'pageIndex': pageIndex,
        'success': True
    }
    return Response(json_util.dumps(extracted, default=json_util.default), status=200, mimetype='application/json')




@api.route("/accounts", methods=["PUT"])
@authMiddleware
@swag_from('docs/add_account.yml')
def add_account():
    request_params = request.form
    if 'email' not in request_params or 'name' not in request_params:
        return Response('Email and name not present in parameters!', status=404, mimetype='application/json')
    try:
        account = Account({
            'email': request_params['email'],
            'name': request_params['name']
        })
        account.save()
    except errors.DuplicateKeyError as e:
        return Response('Duplicate account id!', status=404, mimetype='application/json')
    return Response(json_util.dumps(account), status=200, mimetype='application/json')





@api.route("/accounts/<string:accountid>", methods=["POST"])
@authMiddleware
@swag_from('docs/update_account.yml')
def update_account(accountid):
    request_params = request.form
    if 'email' not in request_params and 'name' not in request_params:
        return Response('Email or name must be present in parameters!', status=404, mimetype='application/json')
    set = {}
    if 'email' in request_params:
        set['email'] = request_params['email']
    if 'name' in request_params:
        set['name'] = request_params['name']
    account = Account({'_id': accountid})
    account.reload()
    account.update(set)
    account.save()
    return Response(json_util.dumps(account), status=200, mimetype='application/json')





@api.route("/accounts/<string:accountid>", methods=["GET"])
@authMiddleware
@swag_from('docs/get_account.yml')
def get_account(accountid):
    account = Account({'_id': accountid})
    account.reload()
    if None == account:
        return Response("account was not found", status=404, mimetype='application/json')
    return Response(json_util.dumps(account), status=200, mimetype='application/json')




@api.route("/accounts/<string:accountid>", methods=["DELETE"])
@authMiddleware
@swag_from('docs/delete_account.yml')
def delete_account(accountid):
    account = Account({'_id': accountid})
    account.remove()
    return Response('', status=200, mimetype='application/json')