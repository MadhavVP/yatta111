from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
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
    
    return jsonify({
        "message": "Subscribed successfully", 
        "user_id": user_id
    }), 201

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
    Returns the two preprocessed bills.
    """
    bills = [
        {
            "id": "1",
            "title": "Confidentiality of pregnancy termination reports.",
            "impact_score": "High",
            "tags": ["reproductive rights"],
            "summary_points": [
                "States that a health care provider's report concerning the performance of an abortion that is submitted to the Indiana department of health is a medical record, confidential, and not subject to disclosure as a public record.",
            ],
            "audio_url": "",
        },
        {
            "id": "2",
            "title": "Maternal health coverage improvements",
            "impact_score": "Medium",
            "tags": ["healthcare", "maternal health"],
            "summary_points": [
                "Grant an exception to a step therapy protocol for a prescription drug prescribed for the treatment of postpartum depression that is not indicated by the federal Food and Drug Administration for postpartum depression on the prescription drug's approved labeling",
                "Provide coverage for biomarker testing for preeclampsia, doula services, mental health screenings, and treatment for maternal mental health",
                "Develop a maternal mental health program. Requires Medicaid pregnancy services to include reimbursement for doula services and biomarker testing for preeclampsia.",
            ],
            "audio_url": "",
        }
    ]
    
    return jsonify(bills)


if __name__ == '__main__':
    # Start Flask server
    print("[Flask] Starting server on http://127.0.0.1:8000")
    app.run(debug=True, port=8000)