import todostorage, textProcessing
File = todostorage.toDoRead()
print(File)
def chatbotread(command):
    chatbotkeys = ["what", "who", "get", "grab", "show", ]
    if textProcessing.inArray(chatbotkeys,command):""""BENS FUNCTION CHECKING IF CHATBOTKEYS ARRAY IS IN FUNCTION"""

