import pyowm, reminderTextProcessing


def equalInArray(array, string): #made by Ben G
    for i in range(0,len(array)):
        if array[i].lower() == string.lower():
            return True
    return False

def detPlace(command): #made by Ben G
    wordsplit = command.split()
    locDetermine = ["at","in","for"]
    for i in range(0,len(wordsplit)):
        if equalInArray(locDetermine, reminderTextProcessing.puncRemove(wordsplit[i].lower())) and i + 1 < len(wordsplit):
            return wordsplit[i + 1]
    return None


def weather(command):
    owm = pyowm.OWM(
        '3e00d7a3b5f712c576e77953d91643f3')

    city = detPlace(command)
    string = ""
    if city != None:
        loc = owm.weather_manager().weather_at_place(city)
        weather = loc.weather

        # temperature
        temp = weather.temperature(unit='celsius')

        for key, val in temp.items():
            string = string + "\n" + (f'{key} => {val}')
    return string
