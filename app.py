from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
import scheduler as my_scheduler
import notifications
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB connection
client = MongoClient(os.environ["MONGO_URI"])
db = client["users"]
users_collection = db["users"]
bills_collection = db["bills"]  # Optional: for storing bills

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sw.js')
def service_worker():
    from flask import send_from_directory
    response = send_from_directory('static', 'sw.js')
    response.headers['Cache-Control'] = 'no-cache'
    return response

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    """
    Endpoint to save user subscription.
    Expected JSON: { "subscription": {...}, "interests": ["tag1", "tag2"] }
    """
    data = request.json
    if not data or 'subscription' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    subscription = data['subscription']
    interests = data.get('interests', [])
    
    # Save to MongoDB
    user_doc = {
        "subscription_info": subscription,
        "tags": interests
    }
    
    result = users_collection.insert_one(user_doc)
    user_id = str(result.inserted_id)
    
    # Send a welcome push
    notifications.send_web_push(subscription, "Welcome! You are subscribed to legislative alerts.")
    
    # Fetch bills for user's interests and create cards
    print(f"[Subscribe] Fetching bills for interests: {interests}")
    new_bills = my_scheduler.fetch_bills_for_tags(interests)
    
    # Save bills to database (avoid duplicates)
    if new_bills:
        for bill in new_bills:
            # Check if bill already exists
            existing = bills_collection.find_one({"id": bill.get("id")})
            if not existing:
                bills_collection.insert_one(bill)
        print(f"[Subscribe] Added {len(new_bills)} new bills to database")
    
    return jsonify({
        "message": "Subscribed successfully", 
        "user_id": user_id,
        "bills_fetched": len(new_bills)
    }), 201

@app.route('/api/trigger-check', methods=['POST'])
def trigger_check():
    """
    Demo Helper: Manually trigger the pipeline.
    """
    print("[API] Manual trigger received.")
    my_scheduler.orchestrate_pipeline()
    return jsonify({"message": "Pipeline triggered manually."}), 200

@app.route('/api/vapid-key', methods=['GET'])
def get_vapid_key():
    """
    Returns the public VAPID key for the frontend.
    """
    public_key = os.getenv("PUBLIC_KEY")
    if not public_key:
         # Fallback for demo if keys aren't generated yet
        return jsonify({"error": "VAPID key not configured"}), 500
    return jsonify({"publicKey": public_key})

@app.route('/api/feed', methods=['GET'])
def get_feed():
    """
    Returns a list of bills based on user sector and state.
    """
    sector = request.args.get('sector')
    state = request.args.get('state')
    tags = request.args.getlist('tags')  # Support filtering by tags
    
    # Build query
    query = {}
    if tags:
        query["tags"] = {"$in": tags}
    
    # Get bills from MongoDB
    bills = list(bills_collection.find(query, {"_id": 0}))
    
    # If no bills in DB, return mock data for demonstration
    if not bills:
        bills = [
            {
                "id": "1",
                "title": "The Safe Staffing Act of 2024",
                "impact_score": "High",
                "tags": ["healthcare", "labor"],
                "summary_points": [
                    "Sets mandatory nurse-to-patient ratios in all state hospitals.",
                    "Prohibits mandatory overtime for nurses except in declared emergencies.",
                    "Requires hospitals to post staffing plans publicly.",
                ],
                "audio_url": "https://www.soundhelix.com/examples/mp3/Soundhelix-Song-1.mp3",
            },
            {
                "id": "2",
                "title": "Fair Scheduling & Wages Ordinance",
                "impact_score": "Medium",
                "tags": ["labor", "service"],
                "summary_points": [
                    "Requires 14-day advance notice for all shift schedules.",
                    "Mandates 'predictability pay' for last-minute schedule changes.",
                    "Increases minimum wage for service workers to $18/hr by 2025.",
                ],
                "audio_url": "",
            },
             {
                "id": "3",
                "title": "Teacher Pay Protection Bill",
                "impact_score": "High",
                "tags": ["education", "labor"],
                "summary_points": [
                    "Guarantees a minimum starting salary of $50,000 for all public school teachers.",
                    "Provides annual cost-of-living adjustments tied to inflation.",
                    "Increases funding for classroom supplies and resources."
                ],
                "audio_url": "",
            }
        ]
        
    return jsonify(bills)


if __name__ == '__main__':
    # Only run initialization once (Flask debug mode runs code twice)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        # This is the reloader process - skip initialization
        pass
    else:
        # First run - do initialization
        print("\n[Startup] Initializing Themis Legislative Alert System...")
        
        # Run pipeline ONCE on startup to populate database
        print("[Startup] Fetching initial bills to populate database...")
        my_scheduler.orchestrate_pipeline()
        
        # Start background scheduler for future updates
        print("[Startup] Starting background scheduler...")
        my_scheduler.start_scheduler()
        
        print("[Startup] Initialization complete!\n")
    
    # Start Flask server
    print("[Flask] Starting server on http://127.0.0.1:8000")
    app.run(debug=True, port=8000)