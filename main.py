# Jim Palomo
# Calendar Application

import sys
from calendar_class import *
from gui import *

'''
TODO: 
1. sort by time
'''

def main(argv):
    calendar = CalendarObject()
    GUI(calendar.DaysOfWeek)    # call GUI object 

if __name__ == '__main__':
    main(sys.argv)
    # print(str(sys.argv))  # first arg is main.pya
    