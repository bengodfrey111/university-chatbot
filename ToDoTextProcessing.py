import todostorage, textProcessing
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

print(chatbotread("what"))

