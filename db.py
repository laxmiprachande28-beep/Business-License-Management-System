
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"

client = MongoClient(MONGO_URI)

db = client["business_license_db"]

applicants = db["applicants"]
applications = db["applications"]
licenses = db["licenses"]
officers = db["officers"]
documents = db["documents"]
payments = db["payments"]
businesses = db["businesses"]
renewals = db["renewals"]

print("MongoDB Connected Successfully!")
print("Database:", db.name)
