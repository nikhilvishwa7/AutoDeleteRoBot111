from pymongo import MongoClient
from config import cfg

# Initialize MongoDB client
mongo_client = MongoClient(cfg.MONGO_URI)
db = mongo_client["AutoDelete"]
collection = db["autodel_data"]

# Save group and time to MongoDB
def save_to_motor_db(group_id, time_in_seconds):
    data = {"group_id": group_id, "time_in_seconds": time_in_seconds, "time_in_minutes": time_in_minutes}
    collection.insert_one(data)

# Retrieve saved time from MongoDB
def get_time_from_motor_db(group_id):
    data = collection.find_one({"group_id": group_id})
    if data:
        return data["time_in_seconds"]
    else:
        return None

# Add other database-related functions here if needed

