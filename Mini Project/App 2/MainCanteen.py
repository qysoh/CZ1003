from tkinter import *
import sys
import time
from datetime import *
from functools import partial
from tkinter import messagebox

class Frames(object):

    def __init__(self):
        pass
 
    def main_frame(self,root):
        root.title("NTU Canteen")
        root.geometry("600x379")
        self.backgroundimage = PhotoImage(file = '/Users/user/Nanyang Technological University/#TAN JUN HAO# - CX1003/Canteen_Info/App/background.png')
        #self.backgroundimage = PhotoImage(file = 'background.png')
        self.nowtime = datetime.now()
        self.newformat = self.nowtime.strftime("%Y-%m-%d %H:%M")
        self.dayname = self.nowtime.strftime("%A") 
        self.timeDisplay = StringVar()
        self.greetings =["Morning","Afternoon","Evening"]
        if(self.nowtime < self.nowtime.replace(hour = 12 ,minute = 0)):
            self.choosegreet = self.greetings[0]                        #Morning
        elif(self.nowtime < self.nowtime.replace(hour = 18 ,minute = 0)):
             self.choosegreet = self.greetings[1]                       #Afternoon
        else:
            self.choosegreet = self.greetings[2]                        #Evening

        self.timeDisplay.set( "Good " + self.choosegreet + "!\nWelcome to NTU North Spine Canteen!\nDate & Time : " + str(self.newformat) + "\nToday: " + str(self.dayname))
        self.timetext = Label(root, textvariable = self.timeDisplay, compound = CENTER, font = "times 20 bold", fg = "#ffc000", image = self.backgroundimage).pack()
        Input_Date = Button(root, text = "Enter date & time", fg = "blue", command = self.Intent_Date).place(x = 90, y = 300)
        Input_Store = Button(root, text = "Show stores avaliable", fg = "blue", command = self.Intent_Store).place(x = 250, y = 300)
        Close_Btn = Button(root, text = "Close", fg = "red", command = root.destroy).place(x=450, y =300)
        self.passintext()

    def passintext(self):
        
        self.StoreList = {}
        eachStore = []
        self.numberOfStalls = 0

        f = open("/Users/user/Nanyang Technological University/#TAN JUN HAO# - CX1003/Canteen_Info/App/Database.txt", "r")
        #f = open("Database.txt", "r")
        contents = f.readlines()
        
        for lines in contents:
            part = lines.split(':')
                   
            if part[0] == "Store" or part[0] == "end":
                if len(eachStore) > 0 or part[0] == "end":
                    self.StoreList["Food" + str(self.numberOfStalls - 1)] = eachStore
                    eachStore = []

                if part[0] != "end":
                    self.StoreList["Store" + str(self.numberOfStalls)] = part[1]
                    self.numberOfStalls += 1
            else:
                dayList = part[4].split(';')

                openingTime = part[2].split('.')
                closingTime = part[3].split('.')

                foodDict = {"Name": part[0],                #name of food item in menu
                            "Price": part[1],               #price of food item
                           "OpenTimeHr": openingTime[0],    #opening time for food
                           "OpenTimeMin": openingTime[1],
                           "CloseTimeHr": closingTime[0],   #closing time for food
                           "CloseTimeMin": closingTime[1],
                           "Days": dayList,                 #days where food is served
                           "AvgTime" : part[5],             #average waiting time
                           "InfoTime_weekday" : part[6],    #weekday opening hours
                           "InfoTime_weekend" : part[7]     #weekend opening hours
                           }
                eachStore.append(foodDict)
           
        #StoreList["Food" + stall no][foodDict]
        #for stalls in range (0,self.numberOfStalls,1):
        #    print(self.StoreList["Store" + str(stalls)])
        #    for each in self.StoreList["Food" + str(stalls)]:
        #        print (each["Name"])
        #        print (each["OpenTimeHr"])
        #        print (each["CloseTimeHr"])
        #    print("\n")

    def Clock_Set(self):
        day_get = int(self.entryday.get())
        month_get = int( self.entrymonth.get())
        min_get = int(self.entrymin.get())
        hour_get = int(self.entryhour.get())
        self.nowtime = self.nowtime.replace(day=day_get, month=month_get, hour=hour_get, minute=min_get)
        self.newformat = self.nowtime.strftime("%Y-%m-%d %H:%M")
        self.dayname = self.nowtime.strftime("%A")
        if(self.nowtime < self.nowtime.replace(hour = 12 ,minute = 0)):
            self.choosegreet = self.greetings[0]
        elif(self.nowtime < self.nowtime.replace(hour = 18 ,minute = 0)):
             self.choosegreet = self.greetings[1]
        else:
            self.choosegreet = self.greetings[2]
        self.timeDisplay.set( "Good " + self.choosegreet + "!\nWelcome to NTU North Spine Canteen!\nDate & Time: " + str(self.newformat) + "\nToday: " + str(self.dayname))
        self.date.destroy()
        
    def Intent_Date(self):
        self.date = Toplevel()
        self.date.title("Set Date and Time")
        self.date.geometry("400x300")
    
        labelday = Label(self.date, text = "Select Date in 2019", font = "Sans 20 bold").grid(row =0, column = 3)
        self.entryday = Spinbox(self.date,from_= 1, to = 31, width = 5)
        self.entryday.grid(row =1, column = 2)
        labelday1 = Label(self.date, text = "Day/Month").grid(row =1, column = 3)
        self.entrymonth = Spinbox(self.date, from_= 1, to = 12, width = 5)
        self.entrymonth.grid(row =1, column = 4)
        labelday = Label(self.date, text = "Select Time (24Hrs)", font = "Sans 20 bold").grid(row =3, column = 3)
        self.entryhour = Spinbox(self.date, from_= 0, to = 23, width = 5)
        self.entryhour.grid(row =4, column = 2)
        labelhour1 = Label(self.date, text = "Hour/Minutes").grid(row =4, column = 3)
        self.entrymin = Spinbox(self.date, from_= 0, to = 59, width = 5)
        self.entrymin.grid(row =4, column = 4)
        Confirm_button = Button(self.date, text = "Confirm", command = self.Clock_Set).grid(row =5 , column =3)
        Close_button = Button(self.date, text = "Exit", fg = "red", command = self.date.destroy).grid(row =5 , column =4)

    def Waiting_Time(self, stalls=0):
        waitingtime = 0
        int_getnum =0
        while True:
                try: 
                    int_getnum = int(self.helpla.get())
                    break
                except ValueError:
                    messagebox.showinfo("Error Message", "Please enter a value between 0-99\nPlease try again!")
                    break

        storeWait = self.StoreList["Food" + str(stalls)][0]["AvgTime"]
       # for i in self.StoreList["Food" + str(stalls)]:
        if(self.nowtime<(self.nowtime.replace(hour = 12 ,minute = 0))): #breakfast
            waitingtime = int(storeWait) * int(int_getnum) * 1
        elif(self.nowtime<(self.nowtime.replace(hour = 18 ,minute = 0))): #lunch
            waitingtime = int(storeWait) * int(int_getnum) * 1.05
        else:                                                              #dinz
            waitingtime = int(storeWait)  * int(int_getnum) * 1.15
        self.waittimeDisplay.set("Current Waiting Time is: " + str(waitingtime) + "min(s)")

    def Intent_Stall_Menu(self,stalls = 0):
        self.menu = Toplevel()
        #self.background = PhotoImage(file = '/Users/user/Nanyang Technological University/#TAN JUN HAO# - CX1003/Canteen_Info/App/pic.png')
        self.menu.configure(background = "light blue")
        self.menu.title(self.StoreList["Store" + str(stalls)])
        self.menu.geometry("650x400")
        Days = ["Monday", "Tuesday" ,"Wednesday","Thursday", "Friday","Saturday","Sunday"]
        counter =0

        for i in self.StoreList["Food" + str(stalls)]: 
            cmptime_open = self.nowtime.replace(hour = int(i["OpenTimeHr"]),minute = int(i["OpenTimeMin"]))
            cmptime_close = self.nowtime.replace(hour = int(i["CloseTimeHr"]),minute = int(i["CloseTimeMin"]))
            self.weekdayInfo = (i["InfoTime_weekday"])
            self.weekendInfo = (i["InfoTime_weekend"])
            #print(self.weekdayInfo)
            if str((Days.index(self.nowtime.strftime("%A")) + 1)) in i["Days"]:
                 
                 if cmptime_open<self.nowtime and cmptime_close>self.nowtime :
                    list1 = Label(self.menu, text = i["Name"], bg = "light blue").grid(row = counter, column = 0)
                    list1 = Label(self.menu, text = i["Price"], bg = "light blue").grid(row = counter, column = 1)
                    counter +=1

        if counter ==0:
            list1 = Label(self.menu, text = "Store Closed!", font = "Times 20 bold", fg = "red", bg = "light blue").grid(row = 1, column = 1)

        else:
            popout_right = Label(self.menu,text = ">>>>>>>>>>>>>",fg = "purple", bg = "light blue").grid(row = counter +1, column =0)
            self.waittimeDisplay = StringVar()
            self.waittimeDisplay.set("")
            waittimeDisplaylabel = Label(self.menu, textvariable = self.waittimeDisplay, font = "calibri 15 bold", bg = "light blue", fg = "purple").grid(row = counter +1, column = 1)
            self.helpla = Entry(self.menu)
            self.helpla.insert(END,"Input no. of pax")
            self.helpla.grid(row = counter +3, column = 1)
            Check_Waiting_Time = Button(self.menu, text = "Calculate Waiting Time", font = "Sans 15", fg = "purple", command = partial(self.Waiting_Time,stalls)).grid(row = counter +3, column = 0)   
      
        weekdaydisplay = Label(self.menu, text = "Operating Hours\nWeekday: "+ self.weekdayInfo, font = "Times 20 bold",fg = "dark blue", bg = "light green").grid (row=10, column=1)
        weekenddisplay = Label(self.menu, text = "Weekend: " + self.weekendInfo, font = "Times 20 bold", fg = "dark blue", bg = "light green").grid (row=11, column=1)
        closebtn = Button(self.menu, text = "Close",font = "Times 20 bold", fg = "red", command =self.menu.destroy).grid (row=9, column=1)

    def Intent_Store(self):
        root = Toplevel()
        root.title("All Stores")
        root.configure(background='light yellow')
        root.geometry("300x300")
        header = Label(root, text = "Please view from the available stores below!", bg = "light yellow")
        header.pack(side = TOP)
        
        for stalls in range (0,self.numberOfStalls,1):
            button_all = Button(root, text =self.StoreList["Store" + str(stalls)], fg = "purple", command = partial(self.Intent_Stall_Menu,stalls)).pack()
        closeBtn = Button(root, text = "Close", fg = "red", command = root.destroy).pack(side = BOTTOM)

root = Tk()
app = Frames()
app.main_frame(root)
root.mainloop()