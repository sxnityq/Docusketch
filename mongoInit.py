from pymongo import MongoClient

from mongoConfig import (HOST, PORT, DATABASE)


client = MongoClient(f"mongodb://{HOST}:{PORT}/")
mongodb = client[DATABASE]
coll = mongodb.MemoryMonitoring
