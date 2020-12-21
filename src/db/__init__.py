import os
from pymongo import MongoClient

host = os.getenv("MONGO_HOST")
port = os.getenv("MONGO_PORT")
dbname = os.getenv("MONGO_DB")

db = MongoClient('mongo', 27017)[dbname]
