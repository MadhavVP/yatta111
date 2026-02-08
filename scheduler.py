# SCHEDULER MODULE
import threading
import time
import os
from pymongo import MongoClient
from notifications import send_web_push

def fetch_bills_for_tags(tags):
    """
    Fetches bills for specific tags (interests).
    This is called when a user subscribes to immediately populate their feed.
    
    Args:
        tags: List of interest tags (e.g., ["healthcare", "labor"])
    
    Returns:
        List of bill dictionaries
    """
    print(f"[Fetch Bills] Searching for bills with tags: {tags}")
    
    bills = []
    
    for tag in tags:
        print(f"[Fetch Bills] Processing tag: {tag}")
        
        # TODO: Replace with actual query to Nathan's legislation scraper API
        # Example API call:
        # response = requests.get(f"http://legislation-api/search?tag={tag}")
        # links = response.json()
        
        links = []  # Placeholder - query Nathan's thing here
        
        if links:
            for link in links:
                # TODO: Replace with actual query to Gabe's summarization API
                # Example API call:
                # response = requests.post("http://summarizer-api/summarize", 
                #                          json={"url": link})
                # summary_data = response.json()
                
                # For now, create a mock bill structure
                bill = {
                    "id": f"bill_{tag}_{len(bills)}",  # Generate unique ID
                    "title": f"Bill related to {tag}",
                    "impact_score": "Medium",
                    "tags": [tag],
                    "summary_points": [
                        f"This is a summary point about {tag}",
                        "More details would come from Gabe's API"
                    ],
                    "audio_url": "",
                    "source_url": link if isinstance(link, str) else ""
                }
                
                bills.append(bill)
    
    print(f"[Fetch Bills] Found {len(bills)} bills for tags {tags}")
    return bills

def orchestrate_pipeline():
    """
    Pipeline execution that:
    1. Fetches all users from MongoDB
    2. For each user, checks their tags
    3. Queries for new legislation (integrate with Nathan's API)
    4. Generates summaries (integrate with Gabe's API)
    5. Sends notifications
    """
    print("Beginning new legislation check")
    
    # Connect to MongoDB
    client = MongoClient(os.environ["MONGO_URI"])
    db = client["users"]
    users_collection = db["users"]
    bills_collection = db["bills"]
    
    # Fetch all users
    cursor = users_collection.find({})
    
    for user in cursor:
        tags = user.get('tags', [])
        subscription_info = user.get('subscription_info')
        
        if not subscription_info:
            print(f"Skipping user - no subscription info")
            continue
        
        print(f"[Pipeline] Checking legislation for user with tags: {tags}")
        
        # Fetch new bills for this user's tags
        new_bills = fetch_bills_for_tags(tags)
        
        # Save new bills to database (avoid duplicates)
        bills_added = 0
        for bill in new_bills:
            existing = bills_collection.find_one({"id": bill.get("id")})
            if not existing:
                bills_collection.insert_one(bill)
                bills_added += 1
                
                # Send notification for this new bill
                notification_message = f"New legislation: {bill.get('title', 'Unknown bill')}"
                send_web_push(subscription_info, notification_message)
        
        if bills_added > 0:
            print(f"[Pipeline] Added {bills_added} new bills and sent notifications")
    
    # Close MongoDB connection
    client.close()
    print("Ending new legislation check")

def scheduled_job():
    """
    Wrapper function that runs the pipeline in a loop with a delay.
    """
    while True:
        orchestrate_pipeline()
        # Sleep for 1 hour between checks (adjust as needed)
        time.sleep(3600)  # 3600 seconds = 1 hour

def start_scheduler():
    """
    Starts the background scheduler thread.
    """
    # Create and start the background thread
    scheduler_thread = threading.Thread(target=scheduled_job, daemon=True)
    scheduler_thread.start()
    print("[SCHEDULER] Started background job - checking every hour.")