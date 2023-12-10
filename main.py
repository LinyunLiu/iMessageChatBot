import sqlite3
from openai import OpenAI
import time
import pyautogui

chat = []
client = OpenAI(api_key='')
conn = sqlite3.connect('/Users/linyunliu/Library/Messages/chat.db')
cur = conn.cursor()
query = (
    'SELECT message.text, message.is_from_me, chat.chat_identifier '
    'FROM chat JOIN chat_message_join ON chat. "ROWID" = chat_message_join.chat_id '
    'JOIN message ON chat_message_join.message_id = message. "ROWID" '
    'WHERE chat.chat_identifier = "+17788225261" and message.is_from_me = 0 '
    'ORDER BY message_date DESC '
    'LIMIT 1;')


def getMessage():
    message = ""
    cur.execute(query)
    for text in cur.fetchall():
        message = text[0]
    return message


def setUpAI():
    chat.append({"role": "user", "content": "From now on you will refer me as Issac, my name is Issac, and your name is"
                                            "Oliver, don't call"
                                            "yourself an AI ever, you are Oliver. Be informal, like you are "
                                            "chitchatting"
                                            "with a friend, talk like a young teenager. if I ask you any restricted"
                                            "questions or anything that is beyond your answering capability, just say "
                                            "somthing like:"
                                            "'I am sorry, I don't know how to response to that"
                                            "haha'"})
    res = client.chat.completions.create(
        messages=chat,
        model="gpt-3.5-turbo")
    res = res.choices[0].message.content.strip()
    chat.append({"role": "assistant", "content": res})


def iMessageTypeAndSend(data):
    pyautogui.typewrite(data)
    pyautogui.press('enter')


print("setting up AI...")
setUpAI()
last_user_message = ""
print("AI is ready to chat\n")

while True:
    user_message = getMessage().strip()

    if user_message != last_user_message:
        print("Message Received")
        last_user_message = user_message
        chat.append({"role": "user", "content": "[respond with short sentence]" + user_message})
        print("Generating Answer...")
        response = client.chat.completions.create(
            messages=chat,
            model="gpt-3.5-turbo")
        msg = response.choices[0].message.content.strip()
        chat.append({"role": "assistant", "content": msg})

        print("Responding...")
        iMessageTypeAndSend(msg)
        print("\n")

    time.sleep(4)
