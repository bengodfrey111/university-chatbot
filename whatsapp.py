from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import start
  

def readWhatsApp(driver):
    results = driver.find_element_by_class_name("tSmQ1")
    messages = []
    strMessageSplit = list(results.text)
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

# Replace below path with the absolute path 
# to chromedriver in your computer 
target = '"' + input("type the name of a person or group you want the chatbot to be operating in:") + '"'
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
sent = []
while True:
    time.sleep(1)
    lastTime = len(messages) - 1
    messages = readWhatsApp(driver)
    for i in range(lastTime,len(messages), 2):
        print(messages[i])
        response = start.mChatbot(messages[i],"Ben")
        if response != "":
            print(response)
            send(driver, response)
            print(i)
    response = ""
    time.sleep(0.2)
    response = start.reminderChecker()
    if response != "":
        print(response)
        send(driver, response)
    response = ""