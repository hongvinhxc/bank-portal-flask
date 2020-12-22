import os
from pymongo import MongoClient

host = os.getenv("MONGO_HOST")
port = int(os.getenv("MONGO_PORT"))
dbname = os.getenv("MONGO_DB")

db = MongoClient('mongo', port)[dbname]
