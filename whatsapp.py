from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import start
import reminderTextProcessing
  
def puncTimeRemove(string):
    string = string.replace(".","")
    string = string.replace(",","")
    string = string.replace("?","")
    string = string.replace(":","")
    string = string.replace("/","")
    return string

def readWhatsApp(driver):# inefficient but works, its also not as inefficient since whatsapp has a tendicy of unloading old messages
    results = driver.find_element_by_class_name("tSmQ1")
    messages = []
    strMessageSplit = list(results.text) #https://www.youtube.com/watch?v=b5jt2bhSeXs
    string = ""
    for i in range(0,len(strMessageSplit)):
        if strMessageSplit[i] == "\n":
            messages.append(string)
            string = ""
        else:
            string = string + strMessageSplit[i]
    return messages

def send(driver, writing):
    inp_xpath = '//div[@class="DuUXI"]'
    write = driver.find_element_by_xpath(inp_xpath)

    write.send_keys(writing + Keys.ENTER) 

def userDet(messages): #this tries to determine who is currently speaking
    sent = []
    username = ""
    for i in range(0,len(messages)): #trying to find who was the latest user to speak
        noPunc = puncTimeRemove(messages[i])
        if reminderTextProcessing.isInt(noPunc) and (len(noPunc) == 3 or len(noPunc) == 4):
            if len(messages) > i + 2:
                noPunc2 = puncTimeRemove(messages[i + 2])
                if not(reminderTextProcessing.isInt(noPunc2) and (len(noPunc2) == 3 or len(noPunc2) == 4)):
                    username = messages[i + 1]
    return username

# Replace below path with the absolute path 
# to chromedriver in your computer 
target = '"' + input("Which group chat do you want the chatbot to operate in?") + '"'
driver = webdriver.Chrome('chromedriver.exe') #https://www.youtube.com/watch?v=u3CJFt8xWNo
  
driver.get("https://web.whatsapp.com/") 
wait = WebDriverWait(driver, 600) 
  
  
# Replace the below string with your own message 
string = "Chatbot online"
  
x_arg = '//span[@title=' + target + ']'
time.sleep(10) #to wait for the page to finish loading
group_title = driver.find_element_by_xpath(x_arg)
group_title.click() 
send(driver, string)
time.sleep(1)

messages = readWhatsApp(driver)
username = userDet(messages)

while True: #checking if someone wrote something every couple of seconds
    time.sleep(1)
    lastTime = len(messages) - 1
    messages = readWhatsApp(driver)
    username = userDet(messages)
    for i in range(lastTime,len(messages)):
        print(messages[i])
        print(username)
        try: #if there is an error because someone typed something wrongly or it mistook a command then it does nothing instead of crashing
            response = start.mChatbot(messages[i],username)
        except:
            pass
        if response != "" and response != None:
            print(response)
            send(driver, response)
    response = ""
    time.sleep(1)
    try:
        response = start.reminderChecker()
    except:
        pass
    if response != "":
        print(response)
        send(driver, response)
    response = ""