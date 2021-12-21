# calendar-application
> Calendar application starting date on Monday to Sunday. Displays weekly events.
> second version to calendar application, old version archived

#### How to Run
1. Install modules under Modules header
2. Navigate to Google Cloud Platform > https://console.cloud.google.com/
a. Under APIs Header > Go to APIs overview
b. Under APIs & Services > Credentials
c. Under Credentials > Create Credentials for OAuth 2.0 Client IDs
d. Under OAuth 2.0 Client IDs > Actions > DOWNLOAD JSON > Rename JSON to client_secrets.json and move file in main workspace directory
3. navigate to calendar-application directory & open the terminal > type ``make`` (program should open and begin processing)

#### Modules 
> Install using pip
- datetime > ``pip install datetime``
- oauth2client > ``pip install oauth2client``
- googleapiclient > ``pip install googleapiclient``
- PySimpleGUI > ``pip install PySimpleGUI``

#### Notes
- Removed weather widget (causing request issues breaking GUI)
- Sorting events based on time needed

#### Reference Pages 
- Authentication:       https://developers.google.com/calendar/auth
- Reference:            https://developers.google.com/calendar/v3/reference/
- Scopes:               https://developers.google.com/calendar/api/guides/auth
- Sample Authentication: https://github.com/googleapis/google-api-python-client/tree/main/samples/calendar_api