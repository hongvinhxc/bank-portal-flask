from db import db
from models import Model

accounts = db.accounts

class Account(Model):

    collection = accounts

    def count():
        return accounts.count_documents({})
        
    def getList(pageSize, pageIndex):
        return accounts.aggregate([
            {
                "$skip": pageSize*(pageIndex-1) if pageIndex > 0 else 0
            },
            {
                "$limit": pageSize
            }, 
            { 
                "$addFields" :  {
                "_id" : { "$toString": "$_id" }
                }
            }
        ])

