import os
import json 
from pymongo import MongoClient 

host = os.getenv("MONGO_HOST")
port = int(os.getenv("MONGO_PORT"))
dbname = os.getenv("MONGO_DB")

myclient = MongoClient(host, port)

db = myclient[dbname] 

Collection = db["accounts"] 

with open('accounts.json') as file: 
	file_data = json.load(file) 
	
if isinstance(file_data, list): 
	Collection.insert_many(file_data) 
else: 
	Collection.insert_one(file_data) 
