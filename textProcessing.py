import storage
import datetime
import calendar #https://stackoverflow.com/questions/9481136/how-to-find-number-of-days-in-the-current-month
import time
def isInt(variable):
    try:
        variable = int(variable)
        return True
    except ValueError:
        return False

def monthsToYears(monthsAdd):
    months = monthsAdd % 12
    years = int(monthsAdd / 12)
    return months, years

def daysToMonth(daysAdd, time): #this is if the number of days exceed the amount of days in the month
    currentDaysInMonth = calendar.monthrange(time.year, time.month)[1]
    months = 0
    days = daysAdd
    while True:
        months = int(days / currentDaysInMonth)
        days = days % currentDaysInMonth
        months, years = monthsToYears(months)
        monthSec, years = monthsToYears(months + time.month)
        currentDaysInMonth = calendar.monthrange(time.year + years, monthSec)[1]
        if days < currentDaysInMonth:
            break
    
    return days, months
    


def hoursToDays(hoursAdd):
    hours = hoursAdd % 24
    days = int(hoursAdd / 24)
    return hours, days

def minutesToHours(minutesAdd):
    minutes = minutesAdd % 60
    hours = int(minutesAdd / 60)
    return minutes, hours

def dictToDateTime(dict):
    return datetime.datetime(dict["year"], dict["month"], dict["day"], dict["hour"], dict["minute"], 0)

def timeAddition(timeChange, now = datetime.datetime.now()):
    minutes, hours = minutesToHours(timeChange["minute"] + now.minute) #this section just makes the time more convienient to work with (example is 69 minutes will turn into 1 hour and 9 minutes)
    timeChange["minute"] = minutes
    timeChange["hour"] = timeChange["hour"] + hours
    hours, days = hoursToDays(timeChange["hour"] + now.hour)
    timeChange["hour"] = hours
    timeChange["day"] = timeChange["day"] + days
    days, months = daysToMonth(timeChange["day"] + now.day, now)
    timeChange["day"] = days
    timeChange["month"] = timeChange["month"] + months
    months, years = monthsToYears(timeChange["month"] + now.month)
    timeChange["month"] = months
    timeChange["year"] = timeChange["year"] + years + now.year
    return timeChange

def puncRemove(string):
    string = string.replace(".","")
    string = string.replace(",","")
    return string

def addTimeDecipher(numberLoc, words, addTimeLoc): #this will try to get the datetime from the statement if it can from the view that it is saying something like in 3 hours
    addTime = {"minute" : 0, "hour" : 0, "day" : 0, "month" : 0, "year" : 0} #these variables are there in case the user wants a reminder later in a set period of time (example is set reminder in 2 days)
    noPunc = puncRemove(arrayToString(words)).lower()
    if "tommorow" in noPunc: #finding common ways of saying a period of time in the future without writing a number
        addTime["day"] = addTime["day"] + 1
    if "in a day" in noPunc:
        addTime["day"] = addTime["day"] + 1
    if "in an hour" in noPunc:
        addTime["hour"] = addTime["hour"] + 1
    if "in a minute" in noPunc:
        addTime["minute"] = addTime["minute"] + 1
    if "in a month" in noPunc:
        addTime["month"] = addTime["month"] + 1
    if "in a year" in noPunc:
        addTime["year"] = addTime["year"] + 1
    if "next year" in noPunc:
        addTime["year"] = addTime["year"] + 1

        
    if addTimeLoc != None:
        for i in range(0, len(numberLoc)):
            numberInSentence = int(puncRemove(words[numberLoc[i]])) 
            if numberLoc[i] + 1 < len(words):
                if ("minute" in words[numberLoc[i] + 1].lower()): #this determines if there needs to be an addition of times (example could be the number means 3 hours later)
                    addTime["minute"] = numberInSentence + addTime["minute"]
                elif ("hour" in words[numberLoc[i] + 1].lower()):
                    addTime["hour"] = numberInSentence + addTime["hour"]
                elif ("day" in words[numberLoc[i] + 1].lower()):
                    addTime["day"] = numberInSentence + addTime["day"]
                elif ("month" in words[numberLoc[i] + 1].lower()):
                    addTime["month"] = numberInSentence + addTime["month"]
                elif ("year" in words[numberLoc[i] + 1].lower()):
                    addTime["year"] = numberInSentence + addTime["year"]

    return addTime

def isNearMonth(words, numberLoc, months, monthAsNumber): #will try to see if a month is nearby
    if numberLoc + 2 < len(words):
        twoBackAndFoward = words[numberLoc - 2] + words[numberLoc - 1] + words[numberLoc] + words[numberLoc + 1] + words[numberLoc + 2]
        if inArray(months, twoBackAndFoward):
            for i in range(0,len(months)):
                if months[i] in twoBackAndFoward:
                    return monthAsNumber[i] #returns the month as a number
        else:
            return None
    else:
        return None


def inArray(array, string): #will determine if a character in a string is the same as an element of an array
    for i in range(0,len(array)):
        if array[i] in string:
            return True

def timeDetermineFromString(time, timeDetermine, next): #will try and determine the time if the input is the time (written as hour:minute maybe am or pm which will be shown as next for next sentence)
    wordSplit = list(time)
    for i in range(0,len(wordSplit)):
        for j in range(0,len(timeDetermine)):
            if timeDetermine[j] == wordSplit[i]:
                if isInt(wordSplit[i - 1]): #determines the hours of the time
                    hour = wordSplit[i - 1]
                    if isInt(wordSplit[i - 2]):
                        hour = int(wordSplit[i - 2] + hour)
                    if not(int(hour) > 12):
                        if next.lower() == "pm":
                            hour = int(hour) + 12
                            if hour > 23:
                                hour = 0
                if isInt(wordSplit[i + 1]) and isInt(wordSplit[i + 2]): #determines the minutes of the time
                    minute = int(wordSplit[i + 1] + wordSplit[i + 2])
                return minute, hour

    return None, None

def dateDetermineFromString(date, dateDetermine): #will try and determine the date if the input is the date (will be written as days/month/year)
    wordSplit = list(date)
    day = None
    month = None
    year = None
    for i in range(0,len(wordSplit)):
        for j in range(0,len(dateDetermine)):
            if dateDetermine[j] == wordSplit[i]:
                if isInt(wordSplit[i - 1]): #determines the day of date
                    day = wordSplit[i - 1]
                    if isInt(wordSplit[i - 2]):
                        day = int(wordSplit[i - 2] + day)
                if len(wordSplit) > i + 1:
                    if isInt(wordSplit[i + 1]) and isInt(wordSplit[i + 2]): #determines the minutes of the time
                        month = int(wordSplit[i + 1] + wordSplit[i + 2])
                    if inArray(dateDetermine, wordSplit[i + 3]):
                        if isInt(wordSplit[i + 4]) and isInt(wordSplit[i + 5]):
                            year = wordSplit[i + 4] + wordSplit[i + 5]
                            if len(wordSplit) > i + 6:
                                if isInt(wordSplit[i + 6]) and isInt(wordSplit[i + 7]):
                                    year = int(year + wordSplit[i + 6] + wordSplit[i + 7])
                            else:
                                year = int(year) + 2000
                    if day != None and month != None and year != None:
                        return day, month, year

    return None, None, None

def puncYear(word): #this is to determine if there is punctuation in the middle of the number (2020. is very different to 20.20)
    split = word.split()
    punc = [".", ","]
    for i in range(1,len(split) - 1):
        if inArray(punc, split[i]):
            return False
    return True

def removeLetters(string): #removes letters from a string
    string = puncRemove(string)
    letters = "abcdefghijklomnpqrstuvwxyz"
    for i in range(0,len(letters)):
        if letters[i] in string:
            string = string.replace(letters[i],"")
    return string

def specificTimeDecipher(numberLoc, words, specificTimeLoc, timeSection): #will try to determine a specific time that was inputted (example is 1st of jan 2021 will be determined as year = 2021, month = 1, day = 1)
    time = {"minute" : 0, "hour" : 0, "day" : 0, "month" : 0, "year" : 0}
    months = ["jan", "feb", "march", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"]
    monthAsNumber = []
    timeDetermine = [":"] #this is the punctuation that will determine if the time was said (example is 3:30 meaning hour = 3, minute = 30)
    dateAsNumDetermine = ["/", "\\", "."] #punctuation that will determine the date (example would be 3/11/2020 would mean day = 3, month = 1, year = 2020) note it will not be the american format
    for i in range(0,len(months)): #this will act as a way to convert a month into a number (example jan = 1, feb = 2)
        monthAsNumber.append(i + 1)
    if specificTimeLoc != None:
        month = None
        for i in range(0, len(numberLoc)):
            month = isNearMonth(words, numberLoc[i], months, monthAsNumber) #this will determine if the month was mentioned
            if month != None:
                time["month"] = month
                if len(words[numberLoc[i]]) == 4:
                    time["year"] = int(words[numberLoc[i]])
                elif len(words[numberLoc[i]]) == 2 or len(words[numberLoc[i]]) == 1:
                    time["day"] = int(words[numberLoc[i]])
                break

        dateLoc = []
        timeLoc = []
        for i in range(timeSection["start"],timeSection["end"]): #will determine if time is specified and date is specified in number form 
            if time["year"] == 0 and len(puncRemove(words[i])) == 4 and puncYear(words[i]) and isInt(puncRemove(words[i])):
                time["year"] = int(puncRemove(words[i]))
            if inArray(timeDetermine, words[i]):
                timeLoc.append(i)
            if inArray(dateAsNumDetermine, words[i]):
                dateLoc.append(i)
            if isInt(removeLetters(words[i])): #this checks to see if a specific hour has been inputted
                if int(removeLetters(words[i])) <= 12:
                    if "am" in words[i].lower():
                        time["hour"] = int(removeLetters(words[i]))
                    elif "pm" in words[i].lower():
                        time["hour"] = int(removeLetters(words[i])) + 12
                    if i + 1 < len(words):
                        if words[i + 1].lower() == "am":
                            time["hour"] = int(removeLetters(words[i]))
                        elif words[i + 1].lower() == "pm":
                            time["hour"] = int(removeLetters(words[i])) + 12

            if inArray(months, words[i]):
                for j in range(0,len(months)):
                    if months[j] in words[i]:
                        time["month"] = monthAsNumber[j]

            for i in range(0,len(timeLoc)):
                minute, hour = timeDetermineFromString(words[timeLoc[i]], timeDetermine, words[timeLoc[i] + 1])
                if minute != None and hour != None:
                    time["minute"] = minute
                    time["hour"] = hour
                    break
            for i in range(0,len(dateLoc)):
                day, month, year = dateDetermineFromString(words[dateLoc[i]], dateAsNumDetermine)
                if day != None and month != None and year != None:
                    time["day"] = day
                    time["month"] = month
                    time["year"] = year
                    break
        return time
    return time
def arrayToString(array):
    string = str(array[0])
    for i in range(1,len(array)):
        string = " " + str(array[i])
    return string

def reminderStatement(words, reminderSection): #this will put the reminder together as a string
    string = str(words[reminderSection["start"]])
    for i in range(reminderSection["start"] + 1, reminderSection["end"]):
        string = string + " " + words[i]
    return string

def specificTimeClean(specTime, addTime): #this is to make the specific time make sense, for example if you want a reminder at 3 am and its currently at 5pm you want 3 am the next day not the same day
    now = datetime.datetime.now()
    if specTime["hour"] != 0 and addTime["day"] == 0 and specTime["day"] == 0 and now.hour > specTime["hour"]:
        addTime["day"] = addTime["day"] + 1
    if specTime["month"] != 0 and addTime["year"] == 0 and specTime["year"] == 0 and now.month > specTime["month"]:
        addTime["year"] = addTime["year"] + 1
    return addTime


def setReminder(command, user, write = True):
    words = command.split()
    numberLoc = []
    time = {"minute" : 0, "hour" : 0, "day" : 0, "month" : 0, "year" : 0}
    reminderStatementIndicator = ["that", "to"] #specific words that will indicate that the user will actually say their reminder (example: user may say remind me at ... to <insert reminder>)
    TimeIndicator = ["at","in","for"]
    startStateLoc = None #this is where the first word of the actual reminder starts
    TimeLoc = None
    for i in range(0,len(words)):
        if words[i] in TimeIndicator and TimeLoc == None: #this will try to find where the time will be said
            TimeLoc = i
        elif words[i] in reminderStatementIndicator and startStateLoc == None: #this will try to find where the actual reminder starts
            startStateLoc = i

    timeSection = {"start" : 0, "end" : 0} #tjis will be the beggining and the end section of the time section of the sentence
    reminderSection = {"start" : 0, "end" : 0} #this will be the beggining and the end of the reminder section of the sentence
    if TimeLoc != None:
        if startStateLoc > TimeLoc:
            timeSection["start"] = 0
            timeSection["end"] = startStateLoc + 1
            reminderSection["start"] = startStateLoc
            reminderSection["end"] = len(words)
        else:
            timeSection["start"] = TimeLoc
            timeSection["end"] = len(words)
            reminderSection["start"] = startStateLoc
            reminderSection["end"] = TimeLoc + 1
        for i in range(timeSection["start"],timeSection["end"]): #this determines where the numbers are located in the sentence the user has inputted
            if isInt(puncRemove(words[i])):
                numberLoc.append(i)
    else:
            reminderSection["start"] = startStateLoc
            reminderSection["end"] = len(words)

    addTimeAddition = addTimeDecipher(numberLoc, words, TimeLoc) #this is if time addition is needed
    futureTime = specificTimeDecipher(numberLoc, words, TimeLoc, timeSection) #this is if a specific time is specified
    addTimeAddition = specificTimeClean(futureTime, addTimeAddition)
    now = datetime.datetime.now() #need to do this since you can't have 0 year and 0 month
    futurePlusCurrent = futureTime
    if futurePlusCurrent["hour"] == 0:
        futurePlusCurrent["hour"] = now.hour
    if futurePlusCurrent["day"] == 0:
        futurePlusCurrent["day"] = now.day
    if futurePlusCurrent["month"] == 0:
        futurePlusCurrent["month"] = now.month
    if futurePlusCurrent["year"] == 0:
        futurePlusCurrent["year"] = now.year
    
    time = timeAddition(addTimeAddition, dictToDateTime(futurePlusCurrent)) #adding them since people may have specified some parts of the desired time and not specified the other parts
    reminder = reminderStatement(words, reminderSection)
    timeSentence = reminderStatement(words, timeSection) #just to check where the program thinks the time is
    dateTime = dictToDateTime(time)
    reminderSplit = reminder.split() #just to get rid of an unneccsary word that sometime comes up at the end
    if inArray(TimeIndicator, reminderSplit[len(reminderSplit) - 1]):
        reminderSection["end"] = reminderSection["end"] - 1
        reminder = reminderStatement(words, reminderSection)

    obj = storage.reminder(user, str(dateTime), reminder) #needed to make datetime a string since I wasn't using milliseconds and so doing it this way makes it easier to add that in

    if write == True:
        storage.appendReminder(obj)

    return str(dateTime), reminder, timeSentence


#
def demandReminders(user): #will list all the reminders that the user has if the user asks for it
    reminderObjList = storage.userReminderList(user)
    if len(reminderObjList) > 0:
        string = str(reminderObjList[0].dateTime) + " " + reminderObjList[0].reminder
        for i in range(0,len(reminderObjList)):
            string = "\n" + str(reminderObjList[i].dateTime) + " " + reminderObjList[i].reminder
        return string
    else:
        return "you haven't got any reminders"



if __name__ == "__main__": #this is just the test of the code, won't be main running file
    datetime, reminder, timeSentence = setReminder("remind me to wake up at 4pm", "Ben", False)
    print(datetime)
    print(reminder)
    print(timeSentence)
    print(demandReminders("Ben13"))
    #timeChange = {"minutes" : 61, "hours" : 0, "days" : 58, "months" : 0, "years" : 0}
    #print(timeAddition(timeChange))
    #day, month, year = dateDetermineFromString("5/12/1995", ["/", "\\", "."])
    #print(day)
    #print(month)
    #print(year)