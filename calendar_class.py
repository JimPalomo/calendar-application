# Jim Palomo
# Calendar Application

from datetime import datetime, timedelta
from oauth2client import client
from googleapiclient import sample_tools

class CalendarObject():
    def __init__(self, argv=""):
        self.service     = None
        self.calList     = []

        self.DaysOfWeek = {
            "Monday"    : [],
            "Tuesday"   : [],
            "Wednesday" : [],
            "Thursday"  : [],
            "Friday"    : [],
            "Saturday"  : [],
            "Sunday"    : []
        }

        self.__process(argv)
                
    def __process(self, argv):
        self.__login(argv)          # login with OAUTH2
        self.__getEvents()          # get events
        self.__removeAllDayEvents() # remove unnecessary all day events
        # TODO: sort events by time
        self.__convert24Hto12H()    # convert time to 12 H 

    def __login(self, argv):
        # Authenticate and construct service.
        self.service, flags = sample_tools.init(
            argv, 'calendar', 'v3', __doc__, __file__,
            scope='https://www.googleapis.com/auth/calendar.readonly')

        try:
            # Obtain Calendars
            page_token = None
            while True:
                calendar_list = self.service.calendarList().list(
                    pageToken=page_token).execute()
                for calendar_list_entry in calendar_list['items']:
                    self.calList.append(calendar_list_entry['id'])
                page_token = calendar_list.get('nextPageToken')
                if not page_token:
                    break

        except client.AccessTokenRefreshError:
            print('The credentials have been revoked or expired, please re-run'
                'the application to re-authorize.')
        
    def __splitEventNames(self, eventName):
        # split long event names into two parts
        if len(eventName) >= 15:
            mid = len(eventName)//2

            while eventName[mid] != " ":
                mid += 1

            eventName = eventName[:mid] + "\n" + eventName[mid:].lstrip()     
        
        return eventName        

    def __getEvents(self):
        # Get start of the week --------------------------------------
        curDate = datetime.now()
        start = curDate - timedelta(days=curDate.weekday())
        end = start + timedelta(days=6)    

        # Get Calendar Events --------------------------------------
        for calendar_id in self.calList:
            events = self.service.events().list(calendarId=calendar_id, timeMin=f"{str(start)[:10]}T00:00:00-05:00", timeMax=f"{str(end)[:10]}T23:59:59-05:00", singleEvents=True).execute()['items']

            for event in events:
                eventDetails = {
                    "name"      : "",
                    "start"     : "",
                    "end"       : "",
                    "startTime" : "",
                    "endTime"   : ""
                }   

                # if date and time is given
                if "dateTime" in event["start"]:
                    eventName = self.__splitEventNames(event['summary'])
                    eventDetails.update({"name" : eventName})
                    eventDetails.update({"start" : str(event['start']['dateTime']).split("T")[0]})
                    eventDetails.update({"end" : str(event['end']['dateTime']).split("T")[0]})
                    eventDetails.update({"startTime" : str(event['start']['dateTime'].split("T").pop(1).split("-")[0])})
                    eventDetails.update({"endTime" : str(event['end']['dateTime'].split("T").pop(1).split("-")[0])})

                else:  # only date given, no time
                    eventName = self.__splitEventNames(event['summary'])
                    eventDetails.update({"name" : eventName})
                    eventDetails.update({"start" : event['start']['date']})
                    eventDetails.update({"end" : event['end']['date']})
                    eventDetails.update({"startTime" : ""})
                    eventDetails.update({"endTime" : ""})


                year = int(eventDetails["start"][:4])
                month = int(eventDetails["start"][5:7])
                day = int(eventDetails["start"][8:10])

                # get name of the provided date --------------------------------------
                nameOfDay = datetime(year, month, day).strftime('%A')

                # Determine if event spans X number of days --------------------------------------
                startDay = datetime(int(eventDetails["start"][:4]), int(eventDetails["start"][5:7]), int(eventDetails["start"][8:10]))
                endDay = datetime(int(eventDetails["end"][:4]), int(eventDetails["end"][5:7]), int(eventDetails["end"][8:10]))
                timeSpan = (endDay - startDay).days

                # if events span only one day and ends on the same day --------------------------------------
                # if (eventDetails["start"][8:10] == eventDetails["end"][8:10] or timeSpan == 1) and ("Forecast" not in eventDetails["name"]):    # if dates match (e.g. 2020-12-30) & not forecast
                if timeSpan <= 1:
                    self.DaysOfWeek[nameOfDay].append({
                        "name"      : eventDetails["name"], 
                        "start"     : eventDetails["start"], 
                        "end"       : eventDetails["end"],
                        "startTime" : eventDetails["startTime"],
                        "endTime"   : eventDetails["endTime"]
                        })
                    
                else:   # event spans multiple days --------------------------------------
                    # endYear = int(eventDetails["start"][:4])
                    # endMonth = int(eventDetails["start"][5:7])
                    # endDay = int(eventDetails["start"][8:10])

                    curDate = datetime(year, month, day)
                    dayIndex = 0

                    while dayIndex < 7 and dayIndex < timeSpan:
                        nameOfDay = curDate.strftime("%A")

                        self.DaysOfWeek[nameOfDay].append({
                            "name"  : eventDetails["name"], 
                            "start" : eventDetails["start"], 
                            "end"   : eventDetails["end"],
                            "startTime" : eventDetails["startTime"],
                            "endTime"   : eventDetails["endTime"]                        
                            })
                        
                        curDate = curDate + timedelta(days=1)
                        dayIndex += 1

    def __convert24Hto12H(self):
        for day in self.DaysOfWeek:
            for event in self.DaysOfWeek[day]:
                # check if time is given, if so then convert to 12 Hour scale
                if event["startTime"] != "" and event["endTime"] != "":
                    startTime = event["startTime"].split(":")
                    hour = int(startTime[0])
                    
                    if int(event["startTime"].split(":")[0]) > 12:
                        event["startTime"] = f"{str(hour-12)}:{startTime[1]} PM"
                    else:
                        event["startTime"] = f"{str(hour)}:{startTime[1]} AM"

                    endTime = event["endTime"].split(":")
                    hour = int(endTime[0])
                    if int(event["endTime"].split(":")[0]) > 12:
                        event["endTime"] = f"{str(hour-12)}:{endTime[1]} PM" 
                    else:
                        event["endTime"] = f"{str(hour)}:{startTime[1]} AM"

    def __removeAllDayEvents(self):
        # remove redundant all day events
        # if endTime for an all day event starts on beginning of week then remove
        curDate = datetime.now()
        start = curDate - timedelta(days=curDate.weekday())
        end = start + timedelta(days=6)      

        startOfWeek = start.strftime("%Y-%m-%d")

        sortedDaysOfWeek = {
            "Monday"    : [],
            "Tuesday"   : [],
            "Wednesday" : [],
            "Thursday"  : [],
            "Friday"    : [],
            "Saturday"  : [],
            "Sunday"    : []
        }

        for day in self.DaysOfWeek:  
            for event in self.DaysOfWeek[day]:
                if event["end"] != startOfWeek:
                    sortedDaysOfWeek[day].append(event)
                
        self.DaysOfWeek = sortedDaysOfWeek

    def __sortByTime(self):
        sortedDaysOfWeek = {
            "Monday"    : [],
            "Tuesday"   : [],
            "Wednesday" : [],
            "Thursday"  : [],
            "Friday"    : [],
            "Saturday"  : [],
            "Sunday"    : []
        }

        for day in self.DaysOfWeek:  
            while len(self.DaysOfWeek[day]) != 0:
                for event in self.DaysOfWeek[day]:
                    pass
