# mongo.py

from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/github_webhooks")
client = MongoClient(MONGO_URI)
db = client["github_webhooks"]
events = db["events"]
