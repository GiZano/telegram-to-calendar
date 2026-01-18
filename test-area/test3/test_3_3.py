### ths file is made by ai to learn how to use correctly the google calendar api ###

import os
import json
import datetime
import sys
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- PATH CONFIGURATION ---
# This block ensures the file works regardless of its location (e.g., test-area/test3/)
# It navigates up two directories to find configuration files in the root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))

# Define absolute paths for key files
CREDENTIALS_FILE = os.path.join(project_root, 'credentials.json')
CALENDARS_FILE = os.path.join(project_root, 'calendars.json')
ENV_FILE = os.path.join(project_root, '.env')

# Required Google API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']


# --- HELPER FUNCTIONS ---

def get_calendar_service():
    """Authenticate Service Account and return the service object."""
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ CRITICAL ERROR: Credentials file not found at:\n   {CREDENTIALS_FILE}")
        return None

    try:
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES)
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ Authentication Error: {e}")
        return None

def load_calendars_map():
    """Read calendars.json file and return a dictionary."""
    if not os.path.exists(CALENDARS_FILE):
        print(f"❌ ERROR: calendars.json not found at:\n   {CALENDARS_FILE}")
        return {}
    try:
        with open(CALENDARS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("❌ ERROR: calendars.json is not a valid JSON file.")
        return {}

def create_event_safe(service, calendar_id, event_details):
    print(f"[*] Attempting to import event to Calendar ID: {calendar_id[:10]}...")

    # Generiamo un ID univoco casuale (iCalendar UID)
    import uuid
    uid = f"{uuid.uuid4()}@google.com"

    body = {
        'iCalUID': uid,  # Custom UID to prevent duplicates
        'summary': event_details.get('summary', 'Imported Event'),
        'description': event_details.get('description', ''),
        'start': {
            'dateTime': event_details['start_time'],
            'timeZone': 'Europe/Rome',
        },
        'end': {
            'dateTime': event_details['end_time'],
            'timeZone': 'Europe/Rome',
        },
        'guestsCanModify': True,
    }

    try:
        # Note: Using .import_() instead of .insert() to handle UIDs properly
        event = service.events().import_(calendarId=calendar_id, body=body).execute()
        return event.get('htmlLink')
    except HttpError as e:
        print(f"❌ Google API Error: {e}")
        return None


def force_calendar_refresh(service, calendar_id):
    """
    Change the calendar color to force a UI refresh.
    This helps make new events immediately visible in the Google Calendar UI.
    """
    try:
        # Get the calendar
        calendar = service.calendars().get(calendarId=calendar_id).execute()
        
        # Toggle color (IDs from 1 to 24) to force UI refresh
        current_color = int(calendar.get('colorId', '1'))
        new_color = '2' if current_color == 1 else '1'
        
        calendar['colorId'] = new_color
        
        # Update the calendar
        service.calendars().update(calendarId=calendar_id, body=calendar).execute()
        print("🎨 Calendar color updated (Forced UI refresh)")
    except Exception as e:
        print(f"⚠️ Refresh failed (non-critical): {e}")

# Nel main, dopo create_event_safe:
# link = create_event_safe(...)
# if link:
#     force_calendar_refresh(service, calendar_id)

# --- MAIN TEST ---

def main():
    print("🧪 TEST 3.3 STANDALONE: Event Creation (With Ghosting Fix)\n")
    
    # 1. Load environment
    if os.path.exists(ENV_FILE):
        load_dotenv(ENV_FILE)
    
    # 2. Authentication
    service = get_calendar_service()
    if not service: return

    # 3. Calendar Selection
    calendars_map = load_calendars_map()
    if not calendars_map: return

    # ==============================================================================
    # ⚙️ USER CONFIGURATION (EDIT HERE!)
    # =============================================================================
    
    # A. Which calendar do you want to write to? (Must exist in calendars.json)
    TARGET_KEY = 'xx'  # e.g., 'sport', 'work', 'personal'
    
    # B. Your actual email (the one you use to view the calendar)
    # This is essential for the ghosting fix.
    MY_REAL_EMAIL = 'xx'
    
    # ==============================================================================

    # Validate configuration
    if "xx" in MY_REAL_EMAIL or "@" not in MY_REAL_EMAIL:
        print("🛑 STOP: Please open this file and set your real email in 'MY_REAL_EMAIL'.")
        print("   Without it, the calendar ghosting fix won't work.")
        return

    calendar_id = calendars_map.get(TARGET_KEY)
    if not calendar_id:
        print(f"❌ The key '{TARGET_KEY}' doesn't exist in your calendars.json file.")
        print(f"   Available keys: {list(calendars_map.keys())}")
        return

    print(f"✅ Selected target: {TARGET_KEY.upper()}")

    # 4. Prepare Test Data (For Tomorrow Afternoon)
    domani = datetime.date.today() + datetime.timedelta(days=1)
    
    # Create ISO 8601 formatted times
    start_dt = datetime.datetime.combine(domani, datetime.time(18, 30, 0))  # 18:30
    end_dt = datetime.datetime.combine(domani, datetime.time(19, 30, 0))    # 19:30

    mock_event_data = {
        "summary": "🛠️ Calendar Fix Test",
        "description": "This event includes the 'attendee' fix to prevent calendar ghosting.",
        "start_time": start_dt.isoformat(),
        "end_time": end_dt.isoformat(),
        "user_email": MY_REAL_EMAIL  # Passiamo la tua mail alla funzione
    }

    # 5. Execution
    print("\n🚀 Sending request to Google...")
    link = create_event_safe(service, calendar_id, mock_event_data)
    
    if link:
        force_calendar_refresh(service, calendar_id)

    if link:
        print("\n🎉 SUCCESS! Event created.")
        print(f"🔗 Link: {link}")
        print("👉 Check your calendar: it should be visible without refreshing the page.")
    else:
        print("\n💀 Test Failed.")

if __name__ == '__main__':
    main()