from pywebpush import webpush, WebPushException
import os
import json
from dotenv import load_dotenv

load_dotenv()

VAPID_PRIVATE_KEY = os.getenv("PRIVATE_KEY")
VAPID_CLAIMS = {
    "sub": "mailto:admin@example.com"
}

def send_web_push(subscription_info, message_body):
    """
    Sends a web push notification to a user.
    
    Args:
        subscription_info (dict): The subscription object from the browser.
        message_body (str): The text message to send.
    """
    try:
        webpush(
            subscription_info=subscription_info,
            data=message_body,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS
        )
        print(f"[Notifications] Sent push to user.")
        return True
    except WebPushException as ex:
        print(f"[Notifications] Web Push Failed: {repr(ex)}")
        # In a real app, you might want to remove the subscription if it's 410 (Gone)
        if ex.response and ex.response.status_code == 410:
            print("[Notifications] Subscription expired or removed.")
        return False
    except Exception as e:
        print(f"[Notifications] Unexpected error: {e}")
        return False
