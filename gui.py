# Jim Palomo
# Calendar Application

import PySimpleGUI as sg

from datetime import datetime, timedelta

class GUI():
    def __init__(self, DaysOfWeek):
        self.window = None
        
        self.DaysOfWeek = DaysOfWeek
        
        self.weeklyDate = {
            "Monday"    : "",
            "Tuesday"   : "",
            "Wednesday" : "",
            "Thursday"  : "",
            "Friday"    : "",
            "Saturday"  : "",
            "Sunday"    : ""            
        }

        self.events = {
            "Monday"    : "",
            "Tuesday"   : "",
            "Wednesday" : "",
            "Thursday"  : "",
            "Friday"    : "",
            "Saturday"  : "",
            "Sunday"    : ""
        }
        
        self.__createWindow()

    def __createWindow(self):
        ## Default -------------------------------------------------------
        
        # header
        hd = {"size":(20,2), "text_color":"white", "background_color":"black", 
            "justification":"center", "font":("Firas Sans", "15")}
        
        # event 
        ed = {"size":(20,50), "text_color":"white", "background_color":"black", 
            "justification":"center", "font":("Firas Sans", "15")}

        ## Window and Layout ---------------------------------------------

        # layout
        overlay = [
            [sg.Text(f"""Monday\n{self.weeklyDate["Monday"]}""", key="-MondayDate-", **hd), 
                sg.Text(f"""Tuesday\n{self.weeklyDate["Tuesday"]}""", key="-TuesdayDate-", **hd), 
                sg.Text(f"""Wednesday\n{self.weeklyDate["Wednesday"]}""", key="-WednesdayDate-", **hd), 
                sg.Text(f"""Thursday\n{self.weeklyDate["Thursday"]}""", key="-ThursdayDate-", **hd), 
                sg.Text(f"""Friday\n{self.weeklyDate["Friday"]}""", key="-FridayDate-", **hd), 
                sg.Text(f"""Saturday\n{self.weeklyDate["Saturday"]}""", key="-SaturdayDate-", **hd), 
                sg.Text(f"""Sunday\n{self.weeklyDate["Sunday"]}""", key="-SundayDate-", **hd)],

            [sg.Text(self.events["Monday"], key="-MondayEvent-", **ed), 
                sg.Text(self.events["Tuesday"], key="-TuesdayEvent-", **ed), 
                sg.Text(self.events["Wednesday"], key="-WednesdayEvent-", **ed), 
                sg.Text(self.events["Thursday"], key="-ThursdayEvent-", **ed), 
                sg.Text(self.events["Friday"], key="-FridayEvent-", **ed), 
                sg.Text(self.events["Saturday"], key="-SaturdayEvent-", **ed), 
                sg.Text(self.events["Sunday"], key="-SundayEvent-", **ed), 
                ]                
        ]

        # background layout
        layout = [
            [sg.Column(overlay, justification="center", background_color="black")]
        ]

        # window
        self.window = sg.Window(title="Calendar", layout=layout, background_color="black", return_keyboard_events=True, size=(1920,1080))
        self.window.Finalize()
        self.window.bind("<Escape>", "-ESCAPE-")
        
        self.__mainLoop()

    def __mainLoop(self):
        # event loop --------------------------
        while True:
            self.__update()
            
            # event, values = self.window.read(timeout=10000)     # timeout for 10 s
            event, values = self.window.read(timeout=43200000)  # timeout for 12 H
            
            if event in ("OK", "-ESCAPE-", sg.WIN_CLOSED):
                break

            # clear
            self.weeklyDate = {
                "Monday"    : "",
                "Tuesday"   : "",
                "Wednesday" : "",
                "Thursday"  : "",
                "Friday"    : "",
                "Saturday"  : "",
                "Sunday"    : ""            
            }

            self.events = {
                "Monday"    : "",
                "Tuesday"   : "",
                "Wednesday" : "",
                "Thursday"  : "",
                "Friday"    : "",
                "Saturday"  : "",
                "Sunday"    : ""
            }
            
            self.window.close()
            self.__createWindow()
            
    # update functions ---------
    def __getData(self):
        # update header

        # start of week
        dt = datetime.now()
        curDate = dt - timedelta(days=dt.weekday()) 
        
        for i in range(7):
            date = str(curDate).split(" ")[0].split("-")
            self.weeklyDate[curDate.strftime('%A')] = f"{date[1]}-{date[2]}"

            curDate = curDate + timedelta(days=1)

        # update events
        for day in self.DaysOfWeek:
            for event in self.DaysOfWeek[day]:
                if event["startTime"] != "":
                    self.events[day] += f"""{event["name"]}\n{event["startTime"]} - {event["endTime"]}\n\n"""
                else:
                    self.events[day] += f"""{event["name"]}\n\n"""

    def __update(self):
        # get data from calendar object
        self.__getData()

        # clear gui fields
        for day in self.weeklyDate:
            self.window[f"-{day}Date-"]("")

        for event in self.events:
            self.window[f"-{day}Event-"]("")
            
        # update
        for day, date in self.weeklyDate.items():
            self.window[f"-{day}Date-"].update(value=f"{day}\n{date}")

        for day, event in self.events.items():
            self.window[f"-{day}Event-"].update(value=f"""{self.events[day]}""")

