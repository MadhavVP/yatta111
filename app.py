from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import database
import scheduler as my_scheduler
import notifications
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
    
    # In a real app, use sector and state to filter.
    # For now, we return all matching bills or a mock list if DB is empty.
    
    bills = database.get_all_bills()
    
    # If no bills in DB, return mock data for demonstration
    if not bills:
        bills = [
            {
                "id": "1",
                "title": "The Safe Staffing Act of 2024",
                "impact_score": "High",
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
    # Start the scheduler
    # In production with uWSGI/Gunicorn, this needs careful handling.
    # For hackathon/dev server, this is fine.
    if not os.environ.get("WERKZEUG_RUN_MAIN") == "true": # Prevent double run with reloader
        pass 
    
    # Actually, let's just start it. content of scheduler.py handles the start.
    my_scheduler.start_scheduler()
    
    app.run(debug=True, port=5000)