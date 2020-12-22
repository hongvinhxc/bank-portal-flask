from ..db import db
from . import Model

accounts = db.accounts

class Account(Model):

    collection = accounts

   

