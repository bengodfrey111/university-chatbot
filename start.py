import textProcessing, storage, datetime, threading, time #learnt threading in https://www.tutorialkart.com/python/python-multithreading/

def isDateTimeLarger(dateTime, dateTime2): #since comparing the two datetimes with a simple if statement does not work that well
    if dateTime.year > dateTime2.year: #if datetime is larger than datetime2 then it returns True
        return True
    elif dateTime.year == dateTime2.year:
        if dateTime.month > dateTime2.month:
            return True
        elif dateTime.month == dateTime2.month:
            if dateTime.day > dateTime2.day:
                return True
            elif dateTime.day == dateTime2.day:
                if dateTime.hour > dateTime2.hour:
                    return True
                elif dateTime.hour == dateTime2.hour:
                    if dateTime.minute >= dateTime2.minute:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def reminderChecker(): #this will check if a reminder would need to be displayed
    while True:
        now = datetime.datetime.now()
        reminderObjList = storage.readReminder()
        timedOutLoc = [] #location of the reminders that must be displayed (may or may not be in use)
        for i in range(0,len(reminderObjList)):
            if isDateTimeLarger(now, reminderObjList[i].dateTime):
                print("\n" + reminderObjList[i].user + ": " + reminderObjList[i].reminder)
                timedOutLoc.append(i)
                storage.deleteReminder(reminderObjList, i)
        time.sleep(5) #this delays the code by some seconds so that it won't consume a siginificant amount of cpu power


def initialTextProcess(user):
    while True:
        command = input()
        print(textProcessing.setReminder(command, "Ben"))

if __name__ == "__main__":
    remindCheck = threading.Thread(target=reminderChecker, name="remindCheck") #starts the thread of the reminder checker (depends on how far we get it may or may not be useful)
    remindCheck.start()
    time.sleep(0.1) #delay so that the two threads don't print at the same time
    textCommand = threading.Thread(target=initialTextProcess, name="textCommand", args=("Ben",)) #the user name is just there till we find a better solution
    textCommand.start()