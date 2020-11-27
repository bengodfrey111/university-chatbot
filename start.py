import reminderTextProcessing, ToDoTextProcessing, reminderStorage, datetime, threading, time, weather #learnt threading in https://www.tutorialkart.com/python/python-multithreading/

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
                    if dateTime.minute > dateTime2.minute:
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
    now = datetime.datetime.now()
    reminderObjList = reminderStorage.readReminder()
    timedOutLoc = [] #location of the reminders that must be displayed (may or may not be in use)
    string = ""
    for i in range(0,len(reminderObjList)):
        if isDateTimeLarger(now, reminderObjList[i].dateTime):
            string = string + ("\n" + reminderObjList[i].user + ": " + reminderObjList[i].reminder)
            timedOutLoc.append(i)

    for i in range(0,len(timedOutLoc)):        
        reminderStorage.deleteReminder(reminderObjList, timedOutLoc[i])
    return string

def reminderCheckerAsync():
    while True:
        time.sleep(1)
        reminder = reminderChecker()
        if reminder != "":
            print(reminder)

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
        response = reminderTextProcessing.setReminder(command, user)
    elif ("what" in lCommand and "reminder" in lCommand):
        response = reminderTextProcessing.sayReminders(user)
    elif ("what" in lCommand and "task" in lCommand) or ("list" in lCommand and "task" in lCommand):
        response = ToDoTextProcessing.chatbotread(command)
    elif (reminderTextProcessing.inArray(assignTaskCompleted, lCommand) or reminderTextProcessing.inArray(assignTaskInProgress, lCommand) or reminderTextProcessing.inArray(assignTaskDropped, lCommand)) and "task" in lCommand and reminderTextProcessing.inArray(["1","2","3","4","5","6","7","8","9"],command): #checks if a number is in command
        ToDoTextProcessing.AssignTask(user, command )
    elif "on track" in lCommand and "is" in lCommand and "project" in lCommand:
        response = ToDoTextProcessing.daysDelta()
    elif "weather" in lCommand:
        response = weather.weather(command)
    return response

if __name__ == "__main__":
    remindCheck = threading.Thread(target=reminderCheckerAsync, name="remindCheck") #starts the thread of the reminder checker (depends on how far we get it may or may not be useful)
    remindCheck.start()
    time.sleep(0.1)
    textCommand = threading.Thread(target=inputTest, name="textCommand") #the user name is just there till we find a better solution
    textCommand.start()


#the asyncornous is temporary (just proving reminders are working)