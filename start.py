import textProcessing, storage, datetime, threading, time #learnt threading in https://www.tutorialkart.com/python/python-multithreading/

def reminderChecker(): #this will check if a reminder would need to be displayed
    while True:
        now = datetime.datetime.now()
        reminderObjList = storage.readReminder()
        timedOutLoc = [] #location of the reminders that must be displayed (may or may not be in use)
        for i in range(0,len(reminderObjList)):
            if reminderObjList[i].dateTime < now:
                print("\n" + reminderObjList[i].user + ": " + reminderObjList[i].reminder)
                timedOutLoc.append(i)
                storage.deleteReminder(reminderObjList, i)
        time.sleep(30) #this delays the code by 30 seconds so that it won't consume a siginificant amount of cpu power


def initialTextProcess(user):
    while True:
        command = input()
        print(textProcessing.setReminder(command, "Ben", False))

if __name__ == "__main__":
    remindCheck = threading.Thread(target=reminderChecker, name="remindCheck") #starts the thread of the reminder checker (depends on how far we get it may or may not be useful)
    remindCheck.start()
    time.sleep(0.1) #delay so that the two threads don't print at the same time
    textCommand = threading.Thread(target=initialTextProcess, name="textCommand", args=("Ben",))
    textCommand.start()