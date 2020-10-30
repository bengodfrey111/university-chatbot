import csv
import datetime

class reminder:
    def __init__(self, user, dateTime, reminder): #constructor of all the variables in this object
        self.user = user
        self.dateTime = datetime.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S.%f') #will make the datetime string into a datetime struct (make it easier to get different elements of the date and time)
        self.reminder = reminder

def readReminder():
    file = open("reminders.csv","r")
    csvRead = csv.reader(file,delimiter=",")
    objList = []
    for line in csvRead:
        if line != None and line != "":
            print(line)
            objList.append(reminder(line[0],line[1],line[2]))    #creating the object based on whats contained in the csv file
    file.close()
    return objList

def writeReminder(toWrite): #this will write all the reminders to the reminders file
    fileArray = []
    for i in range(0,len(toWrite)):
        fileArray.append([toWrite[i].user,toWrite[i].dateTime,toWrite[i].reminder]) #this converts the object into a list so that it can be written to the csv file
    file = open("reminders.csv","w",newline="")
    csvWrite = csv.writer(file,delimiter=",")
    csvWrite.writerows(fileArray)
    file.close()

def userReminderList(user):
    objList = readReminder()
    correctUser = []
    for i in range(0,len(objList)):
        if objList[i].user == user:
            correctUser.append(objList[i])
    return correctUser

 
if __name__ == "__main__": #just testing the code (can be ignored)
    objList = readReminder()
    for x in range(0,len(objList)):
        print(objList[x].user)
        print(objList[x].dateTime)
        print(objList[x].reminder)