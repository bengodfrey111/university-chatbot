import textProcessing, ToDoTextProcessing, storage, datetime, threading, time #learnt threading in https://www.tutorialkart.com/python/python-multithreading/

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


def inputTest():
    while True:
        command = input()
        response = mChatbot(command, "Ben")
        print(response)

def mChatbot(command, user):
    response = ""
    lCommand = command.lower()
    assignTaskCompleted = ["complete", "completed", "done", "finished"]
    assignTaskInProgress = ["completing", "started", "starting", "initiating", "doing"]
    assignTaskDropped = ["dropped", "stopped"]
    if "remind me" in lCommand or "set remind" in lCommand:
        response = textProcessing.setReminder(command, user)
    elif ("what" in lCommand and "reminder" in lCommand):
        response = textProcessing.sayReminders(user)
    elif ("what" in lCommand and "task" in lCommand) or ("list" in lCommand and "task" in lCommand):
        response = ToDoTextProcessing.chatbotread(command)
    elif (textProcessing.inArray(assignTaskCompleted, lCommand) or textProcessing.inArray(assignTaskInProgress, lCommand) or textProcessing.inArray(assignTaskDropped, lCommand)) and "task" in lCommand and textProcessing.inArray(["1","2","3","4","5","6","7","8","9"],command): #checks if a number is in command
        ToDoTextProcessing.AssignTask(user, command )
    elif "on track" in lCommand and "is" in lCommand and "project" in lCommand:
        response = ToDoTextProcessing.daysDelta()
    elif "weather" in lCommand:
        pass
    return response

if __name__ == "__main__":
    remindCheck = threading.Thread(target=reminderChecker, name="remindCheck") #starts the thread of the reminder checker (depends on how far we get it may or may not be useful)
    remindCheck.start()
    time.sleep(0.1)
    textCommand = threading.Thread(target=inputTest, name="textCommand") #the user name is just there till we find a better solution
    textCommand.start()


#the asyncornous is temporary (just proving reminders are working)