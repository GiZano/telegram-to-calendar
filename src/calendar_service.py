import os
import json
import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CREDENTIALS_FILE = 'credentials.json'
CALENDARS_FILE   = 'calendars.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    # Service Account auth
    if not os.path.exists(CREDENTIALS_FILE):
        return None
    
    try:
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, 
            scopes=SCOPES
        )
        
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        return None
    
def load_calendars_map():
    # get calendars ids from calendars.json
    if not os.path.exists(CALENDARS_FILE):
        print('Error: unavaiable file calendars.json')
        return {}
    try:
        with open(CALENDARS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print('Error: calendars.json file is not a valid JSON')
        return {}
    
def create_event(service, calendar_id, event_data):   
    # generate random ID
    import uuid
    uid = f"{uuid.uuid4()}@google.com"

    body = {
        'iCalUID': uid,
        'summary': event_data.get('summary'),
        'start': {
            'dateTime': event_data['startDate'],
            'timeZone': 'Europe/Rome'
        },
        'end': {
            'dateTime': event_data['endDate'],
            'timeZone': 'Europe/Rome'
        },
        'guestsCanModify': True
    }

    try:
        event = service.events().import_(calendarId=calendar_id, body=body).execute()
        return event.get('htmlLink')
    except HttpError as e:
        print(f'Error: Google API error {e}')
        return None
        


def add_event(event_data: str):
    # auth
    service = get_calendar_service()
    if not service:
        return

    # choose calendar
    calendars_map = load_calendars_map()
    if not calendars_map: 
        return

    calendar_id = calendars_map[event_data['colorId']]
    if not calendar_id:
        print('Error: specified calendar does not exist')
        return

    my_email = os.getenv('GOOGLE_EMAIL')

    # add missing data
    event_data['user_email'] = my_email

    # execute
    link = create_event(service, calendar_id, event_data)

    if link:
        print(f"INFO: New event at the link: {link}")

    return link
    









        