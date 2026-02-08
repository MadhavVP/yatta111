# Themis

## A web service designed to make legislative information more accessible

Themis helps users stay informed about recently passed or active legislation that directly affects them. By combining user-provided information with real-time legislative data, Themis reports relevant laws and policy changes at the federal and state level.

Users can fill out a form with their interests and demographic information, then receive:
- Informative cards about laws that affect them
- Push notifications when new relevant legislation is passed

## How It Works

1. **Scraping** ([`scraper.py`](scraper.py)): Fetches bills from Indiana General Assembly website
2. **AI Processing** ([`ai_processor.py`](ai_processor.py)): Summarizes bills and extracts relevant tags
3. **Database** ([`database.py`](database.py)): Stores bills and user preferences in MongoDB
4. **Scheduler** ([`scheduler.py`](scheduler.py)): Orchestrates the pipeline, runs every 30 minutes
5. **Notifications** ([`notifications.py`](notifications.py)): Sends web push notifications to matched users
6. **Flask Server** ([`app.py`](app.py)): Serves the frontend and API endpoints

## Setup Instructions

### 1. Clean Up Old Virtual Environments (Optional)

If you have old virtual environments, remove them:

**Windows:**
```powershell
rmdir /s /q .venv .venv2 venv_clean yatta_env 2>nul
```

**macOS/Linux:**
```bash
rm -rf .venv .venv2 venv_clean yatta_env venv
```

### 2. Create a Fresh Virtual Environment

**All platforms:**
```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key dependencies:**
- `flask` - Web framework
- `apscheduler` - Background task scheduling
- `pymongo` - MongoDB database driver
- `pywebpush` - Web push notifications
- `python-dotenv` - Environment variable management
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `selenium` - Web scraping
- `google-generativeai` - AI summarization (if using Gemini)

### 5. Configure Environment Variables

Create a `.env` file in the root directory:

```ini
# MongoDB Connection
MONGODB_URI=your_mongodb_atlas_connection_string

# VAPID Keys (for web push notifications)
PUBLIC_KEY=your_public_vapid_key
PRIVATE_KEY=your_private_vapid_key
VAPID_CLAIM_EMAIL=mailto:admin@example.com

# Gemini API (if using)
GEMINI_API_KEY=your_gemini_api_key
```

**To generate VAPID keys:**
```bash
python -c "from py_vapid import Vapid; v = Vapid(); v.generate_keys(); print('PUBLIC_KEY=' + v.public_key.decode()); print('PRIVATE_KEY=' + v.private_key.decode())"
```

### 6. Run the Application

**Single command to do everything:**

```bash
python3 app.py
```

**What happens when you run this:**

1. **Initial Bill Fetch**: Scrapes bills from Indiana legislature and populates database (runs once on startup)
2. **Background Scheduler**: Sets up recurring job to check for new bills every 30 minutes
3. **Flask Server**: Starts the web server on http://127.0.0.1:8000

**Expected output:**
```
[Database] Connected to MongoDB Atlas
[Startup] Initializing Themis Legislative Alert System...
[Startup] Fetching initial bills to populate database...
[Scheduler] === Starting legislation check ===
[Scraper] Starting bill fetch...
[Scraper] Found: SB 139
[Scraper]   Jury duty exemption for women breastfeeding.
...
[Scheduler] Found 10 new bills to process
[Scheduler] === Legislation check complete ===
[Startup] Starting background scheduler...
[Scheduler] ✓ Background scheduler started (runs every 30 minutes)
[Startup] Initialization complete!
[Flask] Starting server on http://127.0.0.1:8000
 * Running on http://127.0.0.1:8000
 * Debug mode: on
```

### 7. Access the Application

Open your browser and go to:
```
http://localhost:8000
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the frontend |
| `/api/subscribe` | POST | Subscribe to notifications |
| `/api/vapid-key` | GET | Get public VAPID key |
| `/api/feed` | GET | Get bills (with filters) |
| `/api/trigger-check` | POST | Manually trigger bill fetch |

### Example: Subscribe to Notifications

**Request:**
```bash
curl -X POST http://localhost:8000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{
    "subscription": { /* web push subscription object */ },
    "interests": ["reproductive_rights", "healthcare"]
  }'
```

### Example: Manually Trigger Bill Fetch

```bash
curl -X POST http://localhost:8000/api/trigger-check
```

## Testing Notifications

1. Open http://localhost:8000 in your browser
2. Click "Enable Notifications" button
3. Grant notification permission when prompted
4. You should receive a "Welcome!" push notification
5. Trigger the pipeline manually: `curl -X POST http://localhost:8000/api/trigger-check`
6. You should receive a "New Bill" notification if there are matching bills

## Project Structure

```
themis/
├── app.py                  # Flask server & API routes
├── scheduler.py            # Background job orchestration
├── scraper.py             # Bill scraping (Indiana legislature)
├── ai_processor.py        # AI summarization & tagging
├── database.py            # MongoDB interactions
├── notifications.py       # Web push notification system
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── static/                # Frontend assets
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── sw.js             # Service worker for push notifications
└── templates/            # HTML templates
    └── index.html
```

## Development Workflow

### Running with Debug Mode

The app runs with Flask's debug mode enabled by default:
- Auto-reloads when you change code
- Shows detailed error messages
- **Note**: Initialization only runs once (not on reload)

### Running Without Initial Fetch

If you already have data in your database and just want to start the server:

Comment out the initial fetch in `app.py`:
```python
# my_scheduler.orchestrate_pipeline()  # Skip initial fetch
```

### Running Scheduler Only (No Flask)

To just populate the database without starting the web server:

```bash
python3 scheduler.py
```

This is useful for testing the scraper + AI pipeline independently.

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"

Your virtual environment isn't activated. Run:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.bat  # Windows
```

### Bills Are Printing But Server Never Starts

Check that your `scraper.py` has all code inside functions, not at module level.

### MongoDB Connection Error

1. Check your `MONGODB_URI` in `.env`
2. Ensure your IP is whitelisted in MongoDB Atlas
3. Verify your cluster is running

### Selenium/Firefox Issues

1. Install Firefox browser
2. Install geckodriver: `brew install geckodriver` (macOS) or download from Mozilla
3. Make sure geckodriver is in your PATH

### No Notifications Received

1. Check browser console for errors
2. Verify VAPID keys are set in `.env`
3. Ensure you granted notification permission
4. Check that service worker is registered (DevTools > Application > Service Workers)

## Color Scheme

Inspired by InnovateHer's Spring 2026 color scheme:

- `#B04467` - Primary
- `#2F3F5E` - Secondary
- `#FCF5E3` - Background
- `#CBAE51` - Accent
- `#272727` - Text

## Team

- **Sophia**: Flask server + Notifications system
- **Nathan**: Web scraping
- **Gabe**: AI processing
- **Madhav**: Database + Scheduler orchestration

## License

Created for InnovateHer 2026 Hackathon at Purdue University