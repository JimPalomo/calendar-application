# Run Calendar Application

from datetime import datetime
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

## Get Permissions ----------------------------------------------------------------------
scopes = ['https://www.googleapis.com/auth/calendar']               # information on different scopes in README

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
credentials = flow.run_console()

service = build("calendar", "v3", credentials=credentials)

## Get Calendars ------------------------------------------------------------------------
result = service.calendarList().list().execute()
print(result['items'][0])   # prints first calendar

## Get Calendar Events ------------------------------------------------------------------
calendar_id = result['items'][0]['id']                              # print calendar id for first calendar
result = service.events().list(calendarId=calendar_id).execute()
print(result['items'][0])                                           # prints first event

## Get Calendar Events at specific interval ---------------------------------------------
result = service.events().list(calendarId=calendar_id, timeMin="2019-09-14T21:00:00-05:00").execute()
print(result) # print events from 2019-09-14 and onward