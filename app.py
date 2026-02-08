from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import database
import scheduler as my_scheduler
import notifications
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

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
    
    # Save to "Database"
    user_id = database.save_user(subscription, interests)
    
    # Send a welcome push
    notifications.send_web_push(subscription, "Welcome! You are subscribed to legislative alerts.")
    
    return jsonify({"message": "Subscribed successfully", "user_id": user_id}), 201

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
    public_key = os.getenv("VAPID_PUBLIC_KEY")
    if not public_key:
         # Fallback for demo if keys aren't generated yet
        return jsonify({"error": "VAPID key not configured"}), 500
    return jsonify({"publicKey": public_key})


if __name__ == '__main__':
    # Start the scheduler
    # In production with uWSGI/Gunicorn, this needs careful handling.
    # For hackathon/dev server, this is fine.
    if not os.environ.get("WERKZEUG_RUN_MAIN") == "true": # Prevent double run with reloader
        pass 
    
    # Actually, let's just start it. content of scheduler.py handles the start.
    my_scheduler.start_scheduler()
    
    app.run(debug=True, port=5000)