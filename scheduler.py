"""
Scheduler module - orchestrates the legislative alert pipeline
Runs in background without blocking Flask server startup
"""
import time
from apscheduler.schedulers.background import BackgroundScheduler
import scraper
import ai_processor
import database
import notifications
import atexit


def orchestrate_pipeline():
    """
    Main pipeline: Fetch bills -> Process -> Notify users
    This function is CALLED by the scheduler, not run on import!
    """
    print("\n[Scheduler] === Starting legislation check ===")
    
    try:
        # 1. Fetch NEW bills from APIs (Nathan's code)
        print("[Scheduler] Fetching new bills...")
        new_bills = scraper.fetch_new_bills()
        
        if not new_bills:
            print("[Scheduler] No new bills found")
            return
        
        print(f"[Scheduler] Found {len(new_bills)} new bills to process")
        
        # 2. Process each bill
        for bill in new_bills:
            bill_id = bill.get('id')
            print(f"[Scheduler] Processing bill {bill_id}: {bill.get('title')}")
            
            # Get full bill text
            bill_text = bill.get('text', '') or scraper.get_bill_text(bill_id)
            
            # AI processing (Gabe's code)
            summary = ai_processor.summarize(bill_text)
            tags = ai_processor.extract_tags(bill_text)
            
            print(f"[Scheduler]   Tags: {tags}")
            
            # Prepare complete bill data
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
            
            # Save to database (Madhav's code)
            if not database.save_bill(full_bill_data):
                print(f"[Scheduler]   Bill {bill_id} already exists, skipping")
                continue
            
            # Find users interested in these tags
            matching_subscriptions = database.find_matching_users(tags)
            
            if not matching_subscriptions:
                print(f"[Scheduler]   No matching users for bill {bill_id}")
                continue
            
            print(f"[Scheduler]   Notifying {len(matching_subscriptions)} users")
            
            # Create notification payload
            notification_payload = {
                "title": f"New Legislation: {bill.get('title')}",
                "body": summary[:200],
                "url": full_bill_data.get('url', '/'),
                "data": {"bill_id": bill_id, "tags": tags}
            }
            
            # Send notifications (Sophia's code)
            for subscription in matching_subscriptions:
                try:
                    notifications.send_web_push(subscription, notification_payload)
                except Exception as e:
                    print(f"[Scheduler]   Failed to notify user: {e}")
        
        print("[Scheduler] === Legislation check complete ===\n")
        
    except Exception as e:
        print(f"[Scheduler] ERROR in pipeline: {e}")
        import traceback
        traceback.print_exc()


def start_scheduler():
    """
    Start the background scheduler using APScheduler
    This runs in a separate thread and won't block Flask
    """
    scheduler = BackgroundScheduler()
    
    # Schedule the pipeline to run every 30 minutes
    scheduler.add_job(
        func=orchestrate_pipeline,
        trigger="interval",
        minutes=30,
        id='legislation_pipeline',
        replace_existing=True
    )
    
    # Start the scheduler
    scheduler.start()
    print("[Scheduler] ✓ Background scheduler started (runs every 30 minutes)")
    
    # Ensure scheduler shuts down gracefully when app closes
    atexit.register(lambda: scheduler.shutdown())
    
    # Optional: Run once immediately on startup
    # orchestrate_pipeline()
    
    return scheduler