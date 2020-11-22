import csv

def toDoRead():
    file = open("toDoStorage.csv","r")
    csvRead = csv.reader(file,delimiter=",")
    lines = []
    for line in csvRead:
        lines.append(line)
    # lines[line][column]
    toDoList = []
    for i in range(3,len(lines)):
        toDo = {"TaskID" : lines[i][0], "Task" : lines[i][1], "DateStart" : lines[1][2], "DateDue" : lines[1][3], "User" : lines[i][2], "Completed": lines[i][3], "TaskDifficulty" : lines[i][4] }
        toDoList.append(toDo)
    return toDoList


def todoEdit(User, Completed, TaskID):
    file = toDoRead()
    for i in range(len(file)):
        if str(TaskID)==str(file[i]["TaskID"]):
            file[i]["User"] = User
            file[i]["Completed"] = Completed

    toDoWrite(file)


def ToDoSpecific (TaskID):
    File = toDoRead()
    for i in range (0,len(File)):
        if str(TaskID)==str(File[i]["TaskID"]):
            return i+1

def toDoWrite(file): #function created by Ben G
    finalArray = []
    finalArray.append(["","","Date Start", "Date Due"])
    finalArray.append(["","",file[0]["DateStart"], file[0]["DateDue"]])
    finalArray.append(["TaskID", "Task", "UserName", "Completed", "Task Difficulty"])
    for i in range(0,len(file)):
        cLine = file[i]
        finalArray.append([cLine["TaskID"], cLine["Task"], cLine["User"], cLine["Completed"], cLine["TaskDifficulty"]])
    file = open("toDoStorage.csv","w",newline="")
    csvWrite = csv.writer(file,delimiter=",")
    csvWrite.writerows(finalArray)
    file.close()

if __name__ == "__main__":
    TaskID = input("what is taskID")
    print(ToDoSpecific(TaskID))

