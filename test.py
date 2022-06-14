#Test for stock bot
#@author Robert Federline
#@date 6/13/22
#unspagettied as of 6/10/22

import datetime
import time
from bot import bot
import os

os.system("") #makes sure that the ANSI escape sequences work correcly

#ANSI escape sequences for color
COLOR = {
    "YELLOW": "\033[93m",
    "ENDC": "\033[0m",
}

delay = 1 #delay in minutes, can be changed to 5 if internet is being garbage, though you have to quit and rerun the program
#click on the terminal, press ctrl+c (you may have to press it multiple times) 
#change delay & save file, file>save file
#click on terminal again, press the up arrow to get command to run, then hit enter
#command to run should be 'python -m test' 
balance = 500.00 #per stock
time_elapsed = 0 
isOpen = False
x = 1

print("Press CTRL+C to quit")

#getting date
cd = datetime.datetime.now()
cd_string = str(cd)
cd_strings = cd_string.split(" ",1)
cd_strings_date = cd_strings.pop(0)
cd = cd_strings_date.split("-",2)
day_time = cd.pop(2)
day_time = day_time.split(" ",1)
previous_day = day_time.pop(0)

#creating bots
pshg_bot = bot(0,0,"pshg",balance,cd_strings_date)
bmea_bot = bot(0,0,"bmea",balance,cd_strings_date)
iova_bot = bot(0,0,"iova",balance,cd_strings_date)

while x==1:

    #extracting hour and minutes from system datetime
    ct = datetime.datetime.now()
    ct_string = str(ct)
    ct_strings = ct_string.split(" ",1)
    ct_strings_time = ct_strings.pop(1)
    ct_strings_time_units = ct_strings_time.split(":")
    hour = ct_strings_time_units.pop(0)
    minute = ct_strings_time_units.pop(0)

    #checks date and changes file if the day changes
    date = ct_strings.pop(0)
    cd_strings = ct_string.split("-",2)
    day_time = cd_strings.pop(2)
    day_time = day_time.split(" ",1)
    day = day_time.pop(0)
    if (day != previous_day):
        pshg_bot.day_change(date)
        bmea_bot.day_change(date)
        iova_bot.day_change(date)
    previous_day = day

    #checking if the market is open
    if (int(hour)<=9 or int(hour)>=16):
        isOpen = False
    if (((int(hour)==9 and int(minute)>29) or int(hour)>9) and (int(hour)<16)):
        isOpen = True

    #start bots when market opens
    if (int(hour)<=9):
        if (int(hour)==9):
            if (int(minute)>29 and int(minute)<(30+delay)):
                pshg_bot.start()
                bmea_bot.start()
                iova_bot.start()
                time_elapsed = 0
                isOpen = True

    
    #if bot is started after the market opens | for testing purposes: and (int(hour)>=10 or (int(hour)<9))
    if time_elapsed==0:
        pshg_bot.start()
        bmea_bot.start()
        iova_bot.start()


    #alerting user to market status
    if (isOpen==False):
        print(ct,COLOR["YELLOW"],"| CLOSED | The market opens at 9:30 AM",COLOR["ENDC"])
    if (isOpen==True):
        print(ct,COLOR["YELLOW"],"| OPEN | The market closes at 4:00 PM",COLOR["ENDC"])

    #updating bots
    if isOpen==True:
        print(pshg_bot.check_price(time_elapsed,1))
        print(bmea_bot.check_price(time_elapsed,1))
        print(iova_bot.check_price(time_elapsed,1))

    #delay and updates time
    time_elapsed = time_elapsed+delay
    time.sleep(delay*60)
