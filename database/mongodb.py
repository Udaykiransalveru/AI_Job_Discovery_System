from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017/"
)

db = client["AI_Job_Intelligence"]

results_collection = db["results"]