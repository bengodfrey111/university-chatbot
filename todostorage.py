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

File = toDoRead()
def ToDoSpecific (TaskID):
    File = toDoRead()
    for i in range (0,len(File)):
        if str(TaskID)==str(File[i]["TaskID"]):
            return i+1
if __name__ == "__main__":
    TaskID = input("what is taskID")
    print(ToDoSpecific(TaskID))

