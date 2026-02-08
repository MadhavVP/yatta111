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

Or start the scheduler:

```powershell
python scheduler.py
```

## Color Scheme

[Color scheme](https://coolors.co/b04467-2f3f5e-fcf5e3-cbae51-272727):

Inspired by InnovateHer's lovely color scheme for Spring 2026.

- B04467
- 2F3F5E
- FCF5E3
- CBAE51
- 272727
