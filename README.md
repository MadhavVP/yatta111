# Themis

## A webservice designed make legislative information more accessible

### Themis is a web service that helps users stay informed about recently passed or active legislation that directly affects them. By combining user-provided information with real-time legislative data, Themis reports relevant laws and policy changes at the federal and state level that users should know about.

Users can fill out a form on the home page with their username, intrerests and information about groups that they identify with. They will then see informative cards about laws that affect them and can sign up to receive notifications when new laws are passed that affect them.

All user information (username, password, categories) is stored in a MongoDB database referenced in [`scheduler.py`](scheduler.py). We scrape the bill from [`scraper.py`](scraper.py). After finding bills that match keywords, we give it to snowflake to summerize the bills and offload to a json file. We then use the json file to populate info cards on the home page.

## Setup Instructions

### 1. Clean Up Old Virtual Environments

Remove the old virtual environment directories:

```powershell
rmdir /s /q .venv .venv2 venv_clean yatta_env 2>nul
```

This removes all outdated Python virtual environments to prevent conflicts and save disk space.

### 2. Create a Fresh Virtual Environment

Create a new Python virtual environment in the standard `.venv` directory:

```powershell
python -m venv .venv
```

### 3. Activate the Virtual Environment

**On Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**

```cmd
.venv\Scripts\activate.bat
```

**On macOS/Linux:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

Install all required packages from `requirements.txt`:

```powershell
pip install -r requirements.txt
```

The project uses the following dependencies:

- **flask** - Web framework
- **apscheduler** - Task scheduling
- **pymongo** - MongoDB database driver
- **pywebpush** - Web push notifications
- **python-dotenv** - Environment variable management
- **requests** - HTTP requests library

### 5. Run the Application

After activation, you can run the Flask app:

```powershell
python app.py
```
### 3. Configure Environment Variables
1.  Create a `.env` file in the root directory.
2.  Add your VAPID keys (generated via `pywebpush` or online tools):
    ```ini
    PUBLIC_KEY=your_public_key_here
    PRIVATE_KEY=your_private_key_here
    VAPID_CLAIM_EMAIL=mailto:admin@example.com
    ```
    *Note: Do not wrap keys in quotes unless they contain spaces.*

<<<<<<< HEAD
Or start the scheduler:
=======
### 4. Run the Server
Use the python executable inside your venv:
```bash
./venv/bin/python3.14 app.py
```
The server will start on **http://127.0.0.1:8000** (Port 8000 to avoid AirPlay conflict).

## API Endpoints

-   `GET /`: Serves the frontend.
-   `POST /api/subscribe`: Subscribes a user to notifications.
    -   Payload: `{ "subscription": {...}, "interests": ["women", "healthcare"] }`
-   `POST /api/trigger-check`: **(Demo Only)** Manually triggers the bill fetching pipeline.
    -   `curl -X POST http://127.0.0.1:8000/api/trigger-check`

## Testing Notifications
1.  Open `http://localhost:8000`.
2.  Click **"Enable Notifications"**. You should see a "Welcome" push.
3.  Run the manual trigger command above. You should receive a "New Bill" push.
>>>>>>> 04d9d30 (Enhance scheduler with JSON notifications and update docs)

```powershell
python scheduler.py
```

<<<<<<< HEAD
## Color Scheme

[Color scheme](https://coolors.co/b04467-2f3f5e-fcf5e3-cbae51-272727):

Inspired by InnovateHer's lovely color scheme for Spring 2026.

- B04467
- 2F3F5E
- FCF5E3
- CBAE51
- 272727
=======
- `app.py`: Main Flask application and API routes.
- `notifications.py`: Handles sending web push notifications.
- `scheduler.py`: Background job orchestration (Teammate's module).
- `scraper.py`: Fetches bills from external APIs (Teammate's module).
- `ai_processor.py`: Summarizes bill text (Teammate's module).
- `database.py`: Database interactions (Teammate's module).
- `static/`: CSS, JavaScript, and images.
- `templates/`: HTML templates.
>>>>>>> 04d9d30 (Enhance scheduler with JSON notifications and update docs)
