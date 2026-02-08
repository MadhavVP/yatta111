# scheduler.py - Fixed version that tries to combine both
import threading
import time
import os
from pymongo import MongoClient  
from apscheduler.schedulers.background import BackgroundScheduler
import scraper
import ai_processor
import database
import notifications
import atexit

def orchestrate_pipeline():
    """
    Pipeline execution - Bill-first approach (more efficient)
    """
    print("\n[Scheduler] Beginning new legislation check")
    
    try:
        # 1. Fetch NEW bills from APIs (Nathan's code)
        new_bills = scraper.fetch_new_bills()
        
        if not new_bills:
            print("[Scheduler] No new bills found")
            return
        
        print(f"[Scheduler] Found {len(new_bills)} new bills")
        
        # 2. Process each NEW bill
        for bill in new_bills:
            bill_id = bill.get('id')
            
            # Get bill text
            bill_text = bill.get('text', '') or scraper.get_bill_text(bill_id)
            
            # Process with AI (Gabe's code)
            summary = ai_processor.summarize(bill_text)
            tags = ai_processor.extract_tags(bill_text)
            
            print(f"[Scheduler] Bill {bill_id} tags: {tags}")
            
            # Prepare full bill data
            full_bill_data = {
                "id": bill_id,
                "title": bill.get('title'),
                "source": bill.get('source'),
                "state": bill.get('state'),
                "status": bill.get('status'),
                "url": bill.get('url'),
                "summary": summary,
                "tags": tags,
                "processed_at": time.time()
            }
            
            # Save to database (Madhav's database.py)
            if not database.save_bill(full_bill_data):
                print(f"[Scheduler] Bill {bill_id} already exists, skipping")
                continue
            
            # Find users interested in these tags (Madhav's database.py)
            matching_subscriptions = database.find_matching_users(tags)
            
            if not matching_subscriptions:
                print(f"[Scheduler] No matching users for bill {bill_id}")
                continue
            
            print(f"[Scheduler] Found {len(matching_subscriptions)} users for bill {bill_id}")
            
            # Notify each matching user (Sophia's notifications.py)
            notification_payload = {
                "title": f"New Legislation: {bill.get('title')}",
                "body": summary[:200],
                "url": full_bill_data.get('url', '/'),
                "data": {"bill_id": bill_id, "tags": tags}
            }
            
            for subscription in matching_subscriptions:
                notifications.send_web_push(subscription, notification_payload)
        
        print("[Scheduler] Ending new legislation check\n")
        
    except Exception as e:
        print(f"[Scheduler] Error in pipeline: {e}")
        import traceback
        traceback.print_exc()


def start_scheduler():
    """
    Start background scheduler with APScheduler (more reliable than while True)
    """
    scheduler = BackgroundScheduler()
    
    # Run every 30 minutes
    scheduler.add_job(
        func=orchestrate_pipeline,
        trigger="interval",
        minutes=30,
        id='legislation_pipeline',
        replace_existing=True
    )
    
    scheduler.start()
    print("[Scheduler] Background scheduler started (runs every 30 mins)")
    
    # Graceful shutdown
    atexit.register(lambda: scheduler.shutdown())
    
    return scheduler