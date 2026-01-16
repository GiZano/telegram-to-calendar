import os
import json
import datetime
import logging
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

# --- Configuration Constants ---
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'
CALENDARS_CONFIG_FILE = 'calendars.json'

def load_calendar_config(filepath: str) -> Dict[str, str]:
    """
    Loads the calendar mapping from a JSON file.
    
    Returns:
        Dict: A dictionary mapping logical names (e.g., 'sport') to Calendar IDs.
    """
    if not os.path.exists(filepath):
        print(f"[ERROR] Configuration file '{filepath}' not found.")
        return {}
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse '{filepath}': {e}")
        return {}

def get_calendar_service() -> Optional[Any]:
    """
    Authenticates with Google using the Service Account and builds the API client.
    
    Returns:
        The authenticated Google Calendar service object, or None if authentication fails.
    """
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"[CRITICAL] Credentials file '{SERVICE_ACCOUNT_FILE}' not found.")
        return None

    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        print(f"[CRITICAL] Authentication failed: {e}")
        return None

def check_calendar_access(service: Any, name: str, calendar_id: str) -> None:
    """
    Attempts to fetch upcoming events from a specific calendar to verify access permissions.
    """
    print(f"[*] Checking access for: {name.upper()} ({calendar_id})...")
    
    # Use timezone-aware UTC datetime to prevent DeprecationWarning
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    try:
        # Request the next 3 events to minimize payload size during the check
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=3,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            print(f"    [SUCCESS] Access confirmed. No future events found.")
        else:
            print(f"    [SUCCESS] Access confirmed. Found {len(events)} upcoming events:")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', '(No Title)')
                print(f"       -> {start}: {summary}")

    except HttpError as e:
        # Handle specific HTTP errors (e.g., 404 Not Found, 403 Forbidden)
        error_reason = e.content.decode('utf-8') if e.content else "Unknown"
        print(f"    [ERROR] Access Denied or ID Invalid.")
        print(f"    Details: {e.resp.status} - {error_reason}")
        print("    Action Required: Verify the Service Account email is added to this calendar's sharing settings.")
    except Exception as e:
        print(f"    [ERROR] Unexpected error: {e}")

    print("-" * 50)

def main():
    print("--- Google Calendar Bot: Multi-Calendar Access Check ---\n")

    # 1. Initialize API Service
    service = get_calendar_service()
    if not service:
        return

    # 2. Load Calendar Configuration
    calendar_map = load_calendar_config(CALENDARS_CONFIG_FILE)
    if not calendar_map:
        print("[INFO] No calendars configured. Please populate 'calendars.json'.")
        return

    print(f"[INFO] Loaded {len(calendar_map)} calendars from configuration.\n")

    # 3. Iterate through calendars and verify access
    for name, cal_id in calendar_map.items():
        check_calendar_access(service, name, cal_id)

if __name__ == '__main__':
    main()