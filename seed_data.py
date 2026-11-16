from pymongo import MongoClient
from bson import ObjectId
from datetime import date, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client["business_license_db"]

# Clear demo data so this script can safely be run more than once
for name in ["applicants", "applications", "licenses", "officers",
              "documents", "payments", "businesses", "renewals"]:
    db[name].delete_many({})

applicant_id = ObjectId()
officer_id = ObjectId()
application_id = ObjectId()
license_id = ObjectId()
business_id = ObjectId()

db.applicants.insert_one({
    "_id": applicant_id,
    "name": "Aarav Patil",
    "address": "Sangli, Maharashtra",
    "phone": "9876543210",
    "email": "aarav@example.com"
})

db.officers.insert_one({
    "_id": officer_id,
    "name": "Neha Sharma",
    "department": "License Department",
    "phone": "9123456780"
})

db.applications.insert_one({
    "_id": application_id,
    "applicant_id": applicant_id,
    "application_date": date.today().isoformat(),
    "status": "Approved",
    "license_type": "Shop License",
    "business_name": "Aarav General Store"
})

db.documents.insert_one({
    "application_id": application_id,
    "document_type": "Identity Proof",
    "submission_date": date.today().isoformat(),
    "status": "Verified"
})

db.businesses.insert_one({
    "_id": business_id,
    "business_name": "Aarav General Store",
    "business_type": "Retail",
    "address": "Sangli, Maharashtra",
    "phone": "9876543210"
})

db.licenses.insert_one({
    "_id": license_id,
    "application_id": application_id,
    "license_type": "Shop License",
    "issue_date": date.today().isoformat(),
    "expiry_date": (date.today() + timedelta(days=365)).isoformat(),
    "status": "Active",
    "approved_by": officer_id,
    "business_id": business_id
})

db.payments.insert_one({
    "license_id": license_id,
    "amount": 1500,
    "payment_date": date.today().isoformat(),
    "payment_status": "Paid",
    "business_id": business_id
})

db.renewals.insert_one({
    "license_id": license_id,
    "renewal_date": date.today().isoformat(),
    "new_expiry_date": (date.today() + timedelta(days=730)).isoformat(),
    "status": "Pending"
})

print("Sample records inserted into all 8 collections.")
print("Database: business_license_db")
client.close()
