import os
import datetime
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

### READ ONLY ONE CALENDAR BASED ON ID FROM .ENV FILE ###

# 1. Load environment variables
load_dotenv()

# Configuration
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'
CALENDAR_ID = os.getenv("CALENDAR_ID_SCUOLA") 

def get_calendar_service():
    """Authenticates using Service Account and returns the API service."""
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ CRITICAL ERROR: File '{SERVICE_ACCOUNT_FILE}' not found.")
        return None

    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ Authentication Error: {e}")
        return None

def main():
    print("🤖 Calendar Bot: System starting...")

    # Pre-flight check: Verify Environment Variables
    if not CALENDAR_ID:
        print("❌ Error: CALENDAR_ID variable is missing in the .env file!")
        return

    # 2. Authentication
    service = get_calendar_service()
    if not service:
        print("❌ Service initialization failed. Exiting.")
        return

    # 3. Fetch Events
    print(f"📅 Reading Calendar ID: {CALENDAR_ID}")
    
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    try:
        events_result = service.events().list(
            calendarId=CALENDAR_ID, 
            timeMin=now,
            maxResults=10, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])

        if not events:
            print("📭 No future events found (Calendar is clear!).")
        else:
            print(f"✅ Found {len(events)} future events:")
            for event in events:
                # Handle different date formats (all-day events vs specific time)
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'No Title')
                print(f"   🔹 {start}: {summary}")

    except Exception as e:
        print(f"❌ API Error: {e}")
        print("💡 Tip: Ensure the calendar is shared with the Service Account email.")

if __name__ == '__main__':
    main()