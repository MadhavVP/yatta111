# SCHEDULER MODULE
import threading
import time
import os
from pymongo import Mongo

def orchestrate_pipeline():
    """
    Mock pipeline execution.
    In real implementation, this would:
    1. Fetch bills
    2. Process with AI
    3. Save to DB
    4. Notify users
    """
    while True:
        print("Beginning new legislation check")

        client = Mongo(os.environ["MONGO_URI"])
        db = client["users"]
        collection = db["users"]

        cursor = collection.find({})

        for user in cursor:
            tags = user.get('tags', [])
            newlaws = []
            for tag in tags:
                print(tag)
                links = [] #query nathan's thing
                newlaws.append(links)
            for law in newlaws:
                popup = '' #query gabe's thing
                #send a popup to user
                    

        time.sleep(1)
        print("Ending new legislation check")

def start_scheduler():
    """
    Mock scheduler start.
    """
    threading.Thread(target=orchestrate_pipeline)
    print("[MOCK] Scheduler: Started background jobs.")
