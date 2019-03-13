from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import requests
import json
import sys
from time import sleep

sense = SenseHat()

sense.clear()

def loadUsers():
    contents = requests.get("https://randomuser.me/api/?results=10").content
    users = json.loads(contents)
    return users['results']

def loadHistory():
    with open('data.json') as json_data:
        history = json.load(json_data)
        return history

def saveData(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

def like(user, history):
    userObject = { "name": user}

    history['liked'].append(userObject)
    saveData(history)

def dislike(user, history):
    userObject = { "name": user}

    history['disliked'].append(userObject)
    saveData(history)

def main():
    try:
        users = loadUsers()
        for user in users:
            userName = user['name']['first']
            history = loadHistory()
            print(userName)
            sense.show_message(userName)
            event = sense.stick.wait_for_event()
            if(event.direction == 'right'):
                like(userName, history)
            elif(event.direction == 'left'):
                dislike(userName, history)

    except KeyboardInterrupt:
        print('Interrupting process')
        sense.clear()
        sys.exit(0)

main()