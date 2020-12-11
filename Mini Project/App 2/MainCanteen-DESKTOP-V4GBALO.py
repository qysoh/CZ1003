from tkinter import *
import sys
import time
from datetime import *
from functools import partial

class Frames(object):

    def __init__(self):
        pass
 
    def main_frame(self,root):
    
        root.title("NTU Canteen")
        #text = Label(root, text = "noww")
        #clock=Label(root, font=("sans", 25, "bold"), bg= "white")
        #clock.pack(side=TOP)
        
        root.geometry("600x379")
        self.backgroundimage = PhotoImage(file = 'background.png')
        self.nowtime = datetime.now()
        self.dayname = self.nowtime.strftime("%A")
        self.timeDisplay = StringVar()
        self.timeDisplay.set("Welcome to NTU Canteen\nClock Info: " + str(self.nowtime) + "\nDay Now is " + str(self.dayname))
        self.timetext = Label(root, textvariable = self.timeDisplay, compound = CENTER, font = "Times 20 bold", fg = "#ffc000", image = self.backgroundimage).pack()

        #self.label = Label(root,image = self.backgroundimage).pack()
        #self.statusbar = Frame(root)
        #self.statusbar.pack(side="bottom", fill="x", expand=False)
        #clock = Label(root, font = ("times", 40, "bold"), bg = "white").grid(row = 10, column = 10)

        Input_Date = Button(root, text = "Enter date", command = self.Intent_Date).place(x = 200, y = 300)
        Input_Store = Button(root, text = "Show stores avaliable", command = self.Intent_Store).place(x = 400, y = 300)
        
        self.passintext()

    def passintext(self):
        
        self.StoreList = {}
        eachStore = []
        self.numberOfStalls = 0

        f = open("Database.txt", "r")
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

                foodDict = {"Name": part[0], 
                            "Price": part[1],
                           "OpenTimeHr": openingTime[0],
                           "OpenTimeMin": openingTime[1],
                           "CloseTimeHr": closingTime[0],
                           "CloseTimeMin": closingTime[1],
                           "Days": dayList}
                eachStore.append(foodDict)
        
        #StoreList["Food" + stall no][food dictionary]
         
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
        self.dayname = self.nowtime.strftime("%A")
        print(self.nowtime)
        self.timeDisplay.set("Welcome to NTU Canteen\nClock Info: " + str(self.nowtime) + "\nDay Now is " + str(self.dayname))
        
        self.date.destroy()
        
    def Intent_Date(self):
        self.date = Toplevel()
        self.date.title("Set date and time")
        self.date.geometry("400x300")
    
        labelday = Label(self.date, text = "Select Date").grid(row =0, column = 3)
        self.entryday = Spinbox(self.date,from_= 1, to = 31, width = 5)
        self.entryday.grid(row =1, column = 2)


        self.entrymonth = Spinbox(self.date, from_= 1, to = 12, width = 5)
        self.entrymonth.grid(row =1, column = 4)

        labeyear = Label(self.date, text = "2019").grid(row =1, column = 7)

        labelday = Label(self.date, text = "Select Time(24Hrs)").grid(row =3, column = 3)


        self.entryhour = Spinbox(self.date, from_= 0, to = 23, width = 5)
        self.entryhour.grid(row =4, column = 2)
    
        self.entrymin = Spinbox(self.date, from_= 0, to = 59, width = 5)
        self.entrymin.grid(row =4, column = 4)

        Confirm_button = Button(self.date, text = "Confirm", command = self.Clock_Set).grid(row =5 , column =4)
        Close_button = Button(self.date, text = "Exit", command = self.date.destroy).grid(row =5 , column =8)


    #def Waiting_Time(self,stalls):
    #    root = Tk()
    #    root.title(self.StoreList["Store" + str(stalls)])
    #    root.geometry("300x400")

    def Intent_Menu(self,stalls = 0):
        root = Tk()
        root.title(self.StoreList["Store" + str(stalls)])
        root.geometry("300x400")
        Days = ["Monday", "Tuesday" ,"Wednesday","Thursday", "Friday","Saturday","Sunday"]
        counter =0
        for i in self.StoreList["Food" + str(stalls)]: 
            cmptime_open = self.nowtime.replace(hour = int(i["OpenTimeHr"]),minute = int(i["OpenTimeMin"]))
            cmptime_close = self.nowtime.replace(hour = int(i["CloseTimeHr"]),minute = int(i["CloseTimeMin"]))
            if str((Days.index(self.nowtime.strftime("%A")) + 1)) in i["Days"]:
                 
                 if cmptime_open<self.nowtime and cmptime_close>self.nowtime :
                    list1 = Label(root, text = i["Name"]).pack()
                    list1 = Label(root, text = i["Price"]).pack()
                    counter +=1
        waiting_Time_Text = Label(root, text = "Enter waiting time").pack(side = 'bottom')
        Waiting_Time_Entry = Entry(root, text = "Input waiting Time").pack(side='bottom')
        Waiting_Time_Button = Button(root, text = "Confirm").pack

        if counter ==0:
            list1 = Label(root, text = "Close Store").pack()

    def Intent_Store(self):
        root = Tk()
        root.title("All Stores")
        root.geometry("300x500")
        header = Label(root, text = "Please check from the available stores below")
        header.pack(side = TOP)
        
        for stalls in range (0,self.numberOfStalls,1):
            button_mac = Button(root, text =self.StoreList["Store" + str(stalls)], command = partial(self.Intent_Menu,stalls)).pack()



root = Tk()
app = Frames()
app.main_frame(root)
root.mainloop()