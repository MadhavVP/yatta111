# 🏛️ Legislative Notification App

A hackathon project to alert users about new bills affecting them.

## 🚀 Setup Instructions

Follow these steps to get the project running on your local machine.

### 1. Prerequisites
- Python 3.10+
- `pip` (Python package manager)

### 2. Create a Virtual Environment

It's best to run this project in a virtual environment to manage dependencies.

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Once your virtual environment is active (you should see `(venv)` in your terminal prompt), install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory. You can copy the example:

```bash
cp .env.example .env
```

Or manually create it with the following keys:

```ini
# .env
FLASK_APP=app.py
FLASK_ENV=development
PRIVATE_KEY=your_generated_private_key
PUBLIC_KEY=your_generated_public_key
VAPID_CLAIM_EMAIL=mailto:admin@example.com
```

**Generate VAPID Keys:**
If you need new VAPID keys for web push, run:
```bash
python -c "from pywebpush import Vapid; v = Vapid(); v.generate_keys(); print(f'Public: {v.public_key}\nPrivate: {v.private_key}')"
```

### 5. Run the Application

Start the Flask server:

```bash
flask run
# OR
python app.py
```

 The app will be available at `http://127.0.0.1:5000`.

## 📂 Project Structure

- `app.py`: Main Flask application and API routes.
- `notifications.py`: Handles sending web push notifications.
- `scheduler.py`: Background job orchestration (Teammate's module).
- `scraper.py`: Fetches bills from external APIs (Teammate's module).
- `ai_processor.py`: Summarizes bill text (Teammate's module).
- `database.py`: Database interactions (Teammate's module).
- `static/`: CSS, JavaScript, and images.
- `templates/`: HTML templates.

## 🛠️ API Endpoints

- `GET /`: Serves the home page.
- `POST /api/subscribe`: Subscribes a user to notifications.
- `POST /api/trigger-check`: Manually triggers the bill checking pipeline (for demos).