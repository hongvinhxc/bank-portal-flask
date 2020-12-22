from ..db import db
from . import Model
import hashlib

users = db.users

class User(Model):

    collection = users

    def checkExist(self):
        password_hashed = hashlib.sha256(str(self.password).encode('utf-8')).hexdigest()
        user = self.collection.find_one({
            "username": self.username
        })
        if user and user["password"] == password_hashed:
            return str(user["_id"])
        return False