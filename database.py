from pymongo import MongoClient
import os

# Using the URI provided by teammate (hardcoded for now as requested, though .env is better)
MONGO_URI = "mongodb+srv://yatta111:yatta111@lega.emqwd7w.mongodb.net/?appName=lega"

try:
    client = MongoClient(MONGO_URI)
    db = client["mydb"]
    print("[Database] Connected to MongoDB Atlas")
except Exception as e:
    print(f"[Database] Connection failed: {e}")
    db = None

def save_user(subscription, interests):
    """
    Saves a user subscription and their interests to MongoDB.
    """
    if db is None: return "mock_id"
    
    users_collection = db["users"]
    user_data = {
        "subscription": subscription,
        "interests": interests
    }
    result = users_collection.insert_one(user_data)
    print(f"[Database] Saved user {result.inserted_id}")
    return str(result.inserted_id)

def save_bill(bill_data):
    """
    Saves a processed bill to MongoDB.
    """
    if db is None: return False

    bills_collection = db["bills"]
    # check if exists to avoid duplicates
    if bills_collection.find_one({"id": bill_data.get("id")}):
        print(f"[Database] Bill {bill_data.get('id')} already exists.")
        return False
    
    result = bills_collection.insert_one(bill_data)
    print(f"[Database] Saved bill {bill_data.get('id')}")
    return True

def find_matching_users(tags):
    """
    Finds users whose interests match the bill tags.
    Returns a list of subscription objects.
    """
    if db is None: return []

    users_collection = db["users"]
    # Check if any user interest is in the bill tags
    query = {"interests": {"$in": tags}}
    
    users = list(users_collection.find(query))
    print(f"[Database] Found {len(users)} users matching tags {tags}")
    
    # Extract just the subscription part
    subscriptions = [u.get('subscription') for u in users if u.get('subscription')]
    return subscriptions
