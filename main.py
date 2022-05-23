# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# from tkinter import *
# from tkinter import ttk


from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import pickle
import json
# import gnosis.xml.pickle
import os
import socket
import sys
import requests

###################################################################
# Functions

def collectFormData():
    # retrieve data for main
    selMain = mainCB.get()

    # retrieve data for dessert
    selDessert = dessertCB.get()

    #retrieve data for drinks
    drinks = list()
    if drinkCB1val.get() == 1:
        drinks.append("Tea")
    if drinkCB2val.get() == 1:
        drinks.append("Coffee")
    if drinkCB3val.get() == 1:
        drinks.append("Espresso")
    if drinkCB4val.get() == 1:
        drinks.append("Still Water")
    if drinkCB5val.get() == 1:
        drinks.append("Sparkling Water")
    if drinkCB6val.get() == 1:
        drinks.append("Smoothie")

    # create dict for daily meal
    meal = {
        "main": selMain,
        "dessert": selDessert,
        "drinks": drinks
    }
    # return daily meal as dictionary to function addMeal()
    return meal

# weekly meals is a global nested dictionary
# sub dictionaries are named after the selected day
# each day contains the meal as a dictionary
weeklyMeals = {}

def addMeal():
    # retrieve current form data for daily meal
    dailyMeal = {}
    dailyMeal = collectFormData()
    # selected day of the week is the name of the sub dictionary
    subDictName = dayCB.get()
    # populate weekly meals
    if len(weeklyMeals)==0:
        weeklyMeals.update({subDictName: dailyMeal})
        messagebox.showinfo("Info", "Your " + subDictName + " meal was added.")
    else:
        recordedDays=weeklyMeals.keys()
        recordedDays=list(recordedDays)
        x=recordedDays.count(subDictName)
        if x>0:
            replaceDay = messagebox.askyesno("Duplicate day", "Do you wish to overwrite " + subDictName + " ?")
            if replaceDay == True:
                weeklyMeals.update({subDictName: dailyMeal})
                messagebox.showinfo("Info", "Your " + subDictName + " meal was added.")
            else:
                pass
        else:
            weeklyMeals.update({subDictName: dailyMeal})
            messagebox.showinfo("Info", "Your " + subDictName + " meal was added.")
    # display dictionary - for test purpose only
    #for x in weeklyMeals:
    #    print(x)
    #    print(weeklyMeals[x])

def iterateNestedDict(weekly):
    newWeekly = "Your current weekly meal plan:\n"
    for a, b in weekly.items():
        # a is a key is the day of the week
        newWeekly = newWeekly + "\n" + str(a) + "\n"
        # b is another dictionary: meal
        for c, d in b.items():
            if isinstance(d, list):
                tempStr = ""
                for e in d:
                    tempStr = tempStr + str(e) + "  "
                newWeekly = newWeekly + str(c) + ":\t" + str(tempStr) + "\n"
            else:
                newWeekly = newWeekly + str(c) + ":\t" + str(d) + "\n"
    # return nested dictionary as formatted string
    return newWeekly

def displayWeekly():
    # Check if a file exists
    # path = "C:\\Users\\angel\\PycharmProjects\\interface01\\"
    path = os.getcwd()
    dateModified = 0
    currentWeekly = ""
    #dir_list = os.listdir(path)
    # find latest text file
    for x in os.listdir():
        # Check if txt file exists
        if x.endswith(".txt"):
            textFileFound = path + "\\" + x
            # get date of last modification
            timestampMod = os.path.getmtime(textFileFound)
            if timestampMod > dateModified:
                dateModified = timestampMod

    if dateModified > 0:
        # open newest text file
        for x in os.listdir():
            if x.endswith(".txt"):
                textFileFound = path + "\\" + x
                if os.path.getmtime(textFileFound) == dateModified:
                    if "binary" in textFileFound:
                        # Read binary file
                        f = open(textFileFound, "rb")
                        binBuffer = pickle.load(f)
                        currentWeekly = iterateNestedDict(binBuffer)
                        messagebox.showinfo("Weekly Meal Plan", currentWeekly)
                        f.close()
                    elif "JSON" in textFileFound:
                        # read JSON file
                        f = open(textFileFound, "r")
                        buffer = json.loads((f.read()))
                        # loop through nested dictionary to create output text
                        currentWeekly = iterateNestedDict(buffer)

                        messagebox.showinfo("Weekly Meal Plan", currentWeekly)
                        f.close()
                    elif "XML" in textFileFound:
                        pass
                        # Read XML file
                        #f = open(textFileFound, "r")
                        #xmlBuffer = gnosis.xml.pickle.loads((f.read()))
                        # loop through nested dictionary to create output text
                        #currentWeekly = iterateNestedDict(xmlBuffer)
                        #messagebox.showinfo("Weekly Meal Plan", currentWeekly)
                        #f.close()
                    else:
                        # alert user that session is empty and no weekly plan saved so far
                        currentWeekly = currentWeekly + "\nThere are currently no weekly plans.\nPlease create one."
                        messagebox.showinfo("Weekly Meal Plan", currentWeekly)

    elif len(weeklyMeals) == 0:
        # alert user that session is empty and no weekly plan saved so far
        currentWeekly = currentWeekly + "\nThere are currently no weekly plans.\nPlease create one."
        messagebox.showinfo("Weekly Meal Plan", currentWeekly)
    else:
        # display weekly meals from session
        currentWeekly = iterateNestedDict(weeklyMeals)

        currentWeekly = currentWeekly + "\nPlease save your weekly meal plan to file.\n"
        messagebox.showinfo("Weekly Meal Plan", currentWeekly)

def saveWeekly():
    saveMode=varRB.get()
    saveMode=str(saveMode)
    fileName = "weekly.txt"
    #firstLine="Selected save method is: "

    #switchFirstLine={
    #    1: " binary\n",
    #    2: " JSON\n",
    #    3: " XML\n"
    #}

    switchFilePrefix = {
        "1": "binary",
        "2": "JSON",
        "3": "XML"
    }

    # Create fileName according to selected save mode
    fileName = switchFilePrefix.get(saveMode) + "_" + fileName

    switchParameter= {
        "1": "wb",
        "2": "w",
        "3": "w"
    }

    #firstLine=firstLine + str(saveMode) + switchFirstLine.get(saveMode)

    #f = open(fileName, "w")
    #f.write(firstLine)
    #f.close()

    f = open(fileName, switchParameter.get(str(saveMode)))
    if saveMode == "1":
        pickle.dump(weeklyMeals, f)
    elif saveMode == "2":
        f.write(json.dumps(weeklyMeals))
    else:
        pass
        #f.write(gnosis.xml.pickle.dumps(weeklyMeals))
    f.close()
    messagebox.showinfo("Info", "Your weekly meal plan meal was saved in: " + switchFilePrefix.get(str(saveMode)) + " format.")

    # create client socket
    ip = "127.0.0.1"
    port = 12222
    #bufferSize = 1024

    # create corresponding client
    # !!!!!!!!!! only works if ServerSave.py is started from console !!!!!!!!
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        messagebox.showinfo("Info", "Unable to create socket client.")

    try:
        s.connect((ip, port))
    except socket.error as err:
        messagebox.showinfo("Info", "Please run serverSave.py from console to use this feature.")

    if saveMode == "1":
        msg = pickle.dumps(weeklyMeals)
        #asyncio.run(client_save(msg))
        s.sendall(msg)
    elif saveMode == "2":
        msg = json.dumps(weeklyMeals)
        #asyncio.run(client_save(msg))
        s.sendall(msg.encode())
    else:
        pass
    s.close()

def download():
    
    messagebox.showinfo("Info", "Your weekly meal plan meal was downloaded")

###################################################################


# root window
rootW = Tk()

rootW.geometry("300x550")
rootW.title("Assignment 8")

fTitle = Frame(rootW)
fTitle.pack()
labelTitle = Label(fTitle, text="MY WEEKLY CAFETERIA ", font=50).pack(pady=10)

###################################################################

# Meal frame
fMeal = Frame(rootW)
fMeal.pack()
labelDay = Label(fMeal, text="Select day:")

# combobox for days
selectedDay = StringVar(fMeal, "Monday")
dayCB = Combobox(fMeal, textvariable=selectedDay)
dayCB['values'] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dayCB['state'] = 'readonly'
# dayCB.pack()

labelMain = Label(fMeal, text="Choose main:")
# combobox for mains
selectedMain = StringVar(rootW, "Methi Chicken")
mainCB = Combobox(fMeal, textvariable=selectedMain)
mainCB['values'] = ['Methi Chicken', 'Ackee and Saltfish', 'Achari Lamb', 'Chilli Paneer', 'Thai Red Curry',
                    'Samosa Chaat', 'Thai Green Curry']
mainCB['state'] = 'readonly'
# mainCB.pack()

labelDessert = Label(fMeal, text="Choose dessert:")
# combobox for desserts
selectedDessert = StringVar(rootW, "Chocolate Muffin")
dessertCB = Combobox(fMeal, textvariable=selectedDessert)
dessertCB['values'] = ['Chocolate Muffin', 'Cashew Barfi', 'Trifle', 'Apple Pie', 'Pastel de Nata', 'Bread Pudding',
                       'Banana Bread']
dessertCB['state'] = 'readonly'
# dessertCB.pack()

labelDay.grid(row=0, column=0, sticky=W, pady=2)
labelMain.grid(row=1, column=0, sticky=W, pady=2)
labelDessert.grid(row=2, column=0, sticky=W, pady=2)
dayCB.grid(row=0, column=1, sticky=W, pady=2)
mainCB.grid(row=1, column=1, sticky=W, pady=2)
dessertCB.grid(row=2, column=1, sticky=W, pady=2)

labelDrinks = Label(fMeal, text="Select drinks:")
labelDrinks.grid(row=3, column=0, sticky=W, pady=2)
labelVoid = Label(fMeal, text=" ")
labelVoid.grid(row=3, column=1, sticky=W, pady=2)

# Checkbuttons for drinks
drinkCB1val = IntVar()
drinkCB2val = IntVar()
drinkCB3val = IntVar()
drinkCB4val = IntVar()
drinkCB5val = IntVar()
drinkCB6val = IntVar()
# drinkCBval=[]

drinkCB1 = Checkbutton(fMeal, text="Tea",
                       variable=drinkCB1val,
                       onvalue=1,
                       offvalue=0)

# drinkCB1.pack()
drinkCB2 = Checkbutton(fMeal, text="Coffee",
                       variable=drinkCB2val,
                       onvalue=1,
                       offvalue=0)

# drinkCB2.pack()
drinkCB3 = Checkbutton(fMeal, text="Espresso",
                       variable=drinkCB3val,
                       onvalue=1,
                       offvalue=0)

# drinkCB3.pack()
drinkCB4 = Checkbutton(fMeal, text="Still Water",
                       variable=drinkCB4val,
                       onvalue=1,
                       offvalue=0)

# drinkCB4.pack()
drinkCB5 = Checkbutton(fMeal, text="Sparkling Water",
                       variable=drinkCB5val,
                       onvalue=1,
                       offvalue=0)

# drinkCB5.pack()
drinkCB6 = Checkbutton(fMeal, text="Smoothie",
                       variable=drinkCB6val,
                       onvalue=1,
                       offvalue=0)

# drinkCB6.pack()

drinkCB1.grid(row=4, column=0, sticky=W, pady=2)
drinkCB2.grid(row=5, column=0, sticky=W, pady=2)
drinkCB3.grid(row=6, column=0, sticky=W, pady=2)

drinkCB4.grid(row=4, column=1, sticky=W, pady=2)
drinkCB5.grid(row=5, column=1, sticky=W, pady=2)
drinkCB6.grid(row=6, column=1, sticky=W, pady=2)

# Button to add meal
addMealB = Button(fMeal, text='Add meal', command=addMeal)

labelVoid.grid(row=7, column=0, sticky=W, pady=2)
addMealB.grid(row=7, column=1, sticky=W, pady=10)
labelVoid.grid(row=7, column=2, sticky=W, pady=2)

###################################################################

# save frame
# fSave = Frame(rootW)
# fSave.pack(pady=10)

labelSave = Label(fMeal, text="Save as")

# Radiobuttons for save  mode

varRB = IntVar(fMeal, 1)
rbBinary = Radiobutton(fMeal, text='Binary', variable=varRB, value=1)  # pre-selected
rbJSON = Radiobutton(fMeal, text='JSON', variable=varRB, value=2)
rbXML = Radiobutton(fMeal, text='XML', variable=varRB, value=3)

# Button to save weekly meal plan function
saveWeeklyB = Button(fMeal, text='Save weekly meal plan', command=lambda:saveWeekly())

labelSave.grid(row=8, column=0, sticky=W, pady=10)
rbBinary.grid(row=9, column=0, sticky=W, pady=2)
rbJSON.grid(row=10, column=0, sticky=W, pady=2)
rbXML.grid(row=11, column=0, sticky=W, pady=2)
# labelVoid.grid(row = 11, column = 0, sticky = W, pady = 2)

labelVoid.grid(row=8, column=1, sticky=W, pady=10)
labelVoid.grid(row=9, column=1, sticky=W, pady=2)
labelVoid.grid(row=10, column=1, sticky=W, pady=2)
# labelVoid.grid(row = 10, column = 1, sticky = W, pady = 2)
saveWeeklyB.grid(row=11, column=1, sticky=W, pady=2)

###################################################################

# Output frame
fOutput = Frame(rootW)
fOutput.pack(pady=40)

# Button to display meal function
labelDisplay = Label(fOutput, text="Display weekly meal plan:")
displayMealB = Button(fOutput, text='Display', command=displayWeekly)
# displayMealB.pack()

# Button to download meal function
labelDownload = Label(fOutput, text='Download weekly meal plan:')
downloadMealB = Button(fOutput, text='Download', command=lambda:download())
# downloadMealB.pack()

# Button to close window
labelClose = Label(fOutput, text="Finish and Close:")
closeB = Button(fOutput, text='Close', command=rootW.destroy)
# closeB.pack()

labelDisplay.grid(row=0, column=0, sticky=W, pady=2)
labelDownload.grid(row=1, column=0, sticky=W, pady=2)
labelClose.grid(row=2, column=0, sticky=W, pady=2)
displayMealB.grid(row=0, column=1, sticky=W, pady=2)
downloadMealB.grid(row=1, column=1, sticky=W, pady=2)
closeB.grid(row=2, column=1, sticky=W, pady=2)

###################################################################

rootW.mainloop()
