from pymongo import MongoClient
from config import Config

# MongoDB Connection
client = MongoClient(Config.MONGO_URI)

# Database
db = client[Config.DATABASE_NAME]

# Collections
users = db["users"]
history = db["history"]
favorites = db["favorites"]