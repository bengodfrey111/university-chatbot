import todostorage, reminderTextProcessing, datetime
#File = todostorage.toDoRead()
#print(File)
def chatbotread(command):
    chatbotkeys = ["what", "who", "get", "grab", "show", "task", "list"]
    keysNotStart = ["free", "not started"]
    inProgress = ["in progress"]
    CompletedTasks = ["completed", "done"]
    notCompleted = [""]
    ChatbotFile = ""
    if (reminderTextProcessing.inArray(chatbotkeys, command)):#Ben G FUNCTION
        file = todostorage.toDoRead()
        if reminderTextProcessing.inArray(CompletedTasks,command):
            for i in range(0,len(file)):
                if file[i]["Completed"].lower() == "completed":
                    ChatbotFile = ChatbotFile + "TaskId: " + file[i]["TaskID"] + " Task: " + file[i]["Task"] + " DateStart: " + file[i]["DateStart"] + " DateDue: " + file[i]["DateDue"] + " User: " +  file[i]["User"] + " Completed: " + file[i]["Completed"]+ " TaskDifficulty: " + file[i]["TaskDifficulty"] +"\n"
        elif reminderTextProcessing.inArray(inProgress,command):
            for i in range(0,len(file)):
                if file[i]["Completed"] == "in progress":
                    ChatbotFile = ChatbotFile + "TaskId: " + file[i]["TaskID"] + " Task: " + file[i]["Task"] + " DateStart: " + file[i]["DateStart"] + " DateDue: " + file[i]["DateDue"] + " User: " +  file[i]["User"] + " Completed: " + file[i]["Completed"]+ " TaskDifficulty: " + file[i]["TaskDifficulty"] +"\n"
        else:
            for i in range(0,len(file)):
                if file[i]["Completed"].lower() == "":
                    ChatbotFile = ChatbotFile + "TaskId: " + file[i]["TaskID"] + " Task: " + file[i]["Task"] + " DateStart: " + file[i]["DateStart"] + " DateDue: " + file[i]["DateDue"] + " User: " +  file[i]["User"] + " Completed: " + file[i]["Completed"]+ " TaskDifficulty: " + file[i]["TaskDifficulty"] +"\n"
    return ChatbotFile

def AssignTask(Username, command ):
    completed = ["complete", "completed", "done", "finished"]
    inprogress = ["completing", "started", "starting", "initiating", "doing"]
    taskIDIndicator = ["task"]
    if reminderTextProcessing.inArray(taskIDIndicator, command):
        wordSplit = command.split()
        for i in range(0,len(wordSplit)):
            if reminderTextProcessing.inArray(taskIDIndicator, wordSplit[i].lower()):
                if len(wordSplit) > i + 1:
                    if reminderTextProcessing.isInt(wordSplit[i + 1]):
                        TaskID =  wordSplit[i + 1]
                    elif len(wordSplit) > i + 2:
                        if reminderTextProcessing.isInt(wordSplit[i + 2]):
                            TaskID = wordSplit[i + 2]
                    else:
                        TaskID = None
                else:
                    TaskID = None

    if TaskID != None:
        completedStatus = ""
        if (reminderTextProcessing.inArray(completed, command.lower())):
            completedStatus = "completed"
        elif (reminderTextProcessing.inArray(inprogress, command.lower())):
            completedStatus = "in progress"
        todostorage.todoEdit(Username, completedStatus, TaskID)

def TaskDifCheck(line): #checks if the task difficulty has been inputted correctly (made by Ben G)
    if reminderTextProcessing.isInt(line["TaskDifficulty"]):
        pass
    elif not(reminderTextProcessing.isInt(line["TaskDifficulty"])) and line["TaskID"] != "":
        line["TaskDifficulty"] = 1
    else:
        line["TaskDifficulty"] = 0
    return line

def daysDelta(): #FUNCTION Created by Ben G
    file = todostorage.toDoRead()
    now = datetime.datetime.now()
    now = datetime.datetime(now.year, now.month, now.day) #gets rid of the time since taht won't be needed
    startDay, startMonth, startYear = reminderTextProcessing.dateDetermineFromString(file[0]["DateStart"], ["/", "\\", "."])
    endDay, endMonth, endYear = reminderTextProcessing.dateDetermineFromString(file[0]["DateDue"], ["/", "\\", "."])
    startDate = datetime.datetime(startYear, startMonth, startDay) #all dates for each task has the same times (note year has to be full 2020 not just 20)
    endDate = datetime.datetime(endYear, endMonth, endDay)
    elapsedDays = now - startDate
    maxDays = endDate - startDate
    elapsedDays = (elapsedDays.total_seconds()) / (60*60*24) #makes the only unit of measurement of time I have to work with days
    maxDays = (maxDays.total_seconds()) / (60*60*24)
    

    maxPoints = 0
    currentPoints = 0
    for i in range(0,len(file)): #this counts all the points that are possible to get and the amount of points that have currently been earned
        file[i] = TaskDifCheck(file[i])
        maxPoints = maxPoints + float(file[i]["TaskDifficulty"])
        if "progress" in file[i]["Completed"]:
            currentPoints = currentPoints + (float(file[i]["TaskDifficulty"]) / 2)
        elif "completed" in file[i]["Completed"]:
            currentPoints = currentPoints + float(file[i]["TaskDifficulty"])

    pointsPDay = (maxPoints / maxDays)

    expectedPoints = pointsPDay * elapsedDays


    pointsDelta = currentPoints - expectedPoints
    dayDelta = pointsDelta / pointsPDay
    response = ""
    if dayDelta < 0:
        response = "You are " + str((dayDelta ** 2) ** 0.5) + " days behind"
    else:
        response = "You are " + str(dayDelta) + " days ahead"

    return response


