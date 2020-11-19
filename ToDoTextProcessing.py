import todostorage, textProcessing, datetime
#File = todostorage.toDoRead()
#print(File)
def chatbotread(command):
    chatbotkeys = ["what", "who", "get", "grab", "show", ]
    keysNotStart = ["free", "not started"]
    inProgress = ["in progress"]
    CompletedTasks = ["Completed"]
    ChatbotFile = ""
    if (textProcessing.inArray(chatbotkeys, command)):#Bens FUNCTION
        file = todostorage.toDoRead()
        for i in range(0,len(file)):
            ChatbotFile = ChatbotFile + "TaskId: " + file[i]["TaskID,"] + " Task: " + file[i]["Task"] + " DateStart: " + file[i]["DateStart"] + " DateDue: " + file[i]["DateDue"] + " User: " +  file[i]["User"] + " Completed: " + file[i]["Completed"]+ " TaskDifficulty: " + file[i]["TaskDifficulty"] +"\n"
    return ChatbotFile

def TaskDifCheck(line): #checks if the task difficulty has been inputted correctly (made by Ben G)
    if textProcessing.isInt(line["TaskDifficulty"]):
        pass
    elif not(textProcessing.isInt(line["TaskDifficulty"])) and line["TaskID"] != "":
        line["TaskDifficulty"] = 1
    else:
        line["TaskDifficulty"] = 0
    return line

def daysDelta(): #FUNCTION Created by Ben G
    file = todostorage.toDoRead()
    now = datetime.datetime.now()
    now = datetime.datetime(now.year, now.month, now.day) #gets rid of the time since taht won't be needed
    startDate = datetime.datetime.strptime(file[0]["DateStart"], '%d/%m/%Y') #all dates for each task has the same times (note year has to be full 2020 not just 20)
    endDate = datetime.datetime.strptime(file[0]["DateDue"], '%d/%m/%Y')
    elapsedDays = now - startDate
    maxDays = endDate - startDate
    elapsedDays = (elapsedDays.total_seconds()) / (60*60*24) #makes the only unit of measurement of time I have to work with days
    maxDays = (maxDays.total_seconds()) / (60*60*24)
    
    maxPoints = 0
    currentPoints = 0
    for i in range(0,len(file)):
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

    return dayDelta

print(chatbotread("what"))

