import imessage
import re
import os
import random
import urllib
import urllib.request
from bs4 import BeautifulSoup
import pickle
from pprint import pprint


MESSAGE_CONTENT = 0
GUID = 1

weaponized = False

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class Edgar():
    def __init__(self):
        mem_path = 'obj/memories.pkl'
        if not os.path.exists(mem_path):
            os.makedirs(os.path.dirname(mem_path), exist_ok=True)
            self.memories = {}
            save_obj(self.memories,'memories')
        else:
            self.memories = load_obj('memories')
        song_path = 'obj/songs.pkl'
        if not os.path.exists(song_path):
            os.makedirs(os.path.dirname(song_path), exist_ok=True)
            self.songs = {}
            save_obj(self.songs,'songs')
        else:
            self.songs = load_obj('songs')

        #send_message(self,string,chatid,noRobot=False)
    def send_message(self, string, guid, noRobot=False):
        string = string.replace("'", "")
        string = string.replace('"', '')
        faces = ["<I^_^I>", "<Io_oI>", "<I*_*I>", "<IO_OI>", "<I-_-I>", "<I0_0I>", "<Io_0I>", "<IU_UI>", "<I+_+I>", "<I=_=I>"]
        if not noRobot:
            string = random.choice(faces) + " " + string
        if ";+;chat" not in guid:
            body = """
            osascript -e 'tell application "Messages"
              set targetBuddy to "%s"
              set targetService to id of 1st account whose service type = iMessage
              set textMessage to "%s"
              set theBuddy to participant targetBuddy of account id targetService
              send textMessage to theBuddy
            end tell' """ % (guid, string)
        else:
            body = """
            osascript -e 'tell application "Messages"
              set myid to "%s"
              set textMessage to "%s"
              set theBuddy to a reference to chat id myid
              send textMessage to theBuddy
            end tell' """ % (guid, string)
        print(body)
        os.system(body)

    def here(self, guid):
        msg = "*Beep Boop* I am here!"
        self.send_message(msg, guid)

    def what_am_i(self, guid):
        commands = ["Are you here? - Returns if I am running", "What are you? - Returns with help on how to use me", "Remember <key> is <value> - I will remember this relation", "What is <key> - I search my memories for a relation", "Odds <number> - I will generate 2 random numbers for odds within the range given", "Dog pic - returns a cute dog pic from the internet", "Set song of the week <url> <name> - sets that person's song of the week", "Song of the week <name>/all - gets a specific person/everyone's song of the week"]
        msg = "I am a robot that lives inside of Dans texts. You can call me with @Edgar. \rI currently have the following commands:"
        for i, com in enumerate(commands):
            msg = msg + "\r" + com
        self.send_message(msg, guid)

    def remember(self, guid, string1, string2):
        self.memories[string1.lower()] = string2
        save_obj(self.memories, "memories")
        msg = "Ok, I will remember " + string1 + " is " + string2
        self.send_message(msg, guid)

    def recall(self, guid, string1):
        s1 = string1.lower()
        if s1 in self.memories:
             self.send_message(self.memories[s1], guid)
        else:
            msg = "Sorry, I dont have a memory for " + string1
            self.send_message(msg, guid)

    def set_song(self, guid, song, name):
        if name == 'all':
            msg = "All is reserved, sorry"
            self.send_message(msg, guid)
        else:
            self.songs[name.lower()] = song
            save_obj(self.songs, "songs")
            msg = name + "s song of the week set as " + song
            self.send_message(msg, guid)

    def get_song(self, guid, name):
        s1 = name.lower()
        msg = ''
        if s1 == 'all':
            for key, value in self.songs.items():
                msg = msg + "\r" + key + ": " + value
            msg = msg + "\r *Beep Boop*"
            self.send_message(msg, guid)
        elif s1 in self.songs:
             self.send_message(self.songs[s1], guid)
        else:
            msg = "Sorry, I dont have a song of the week for " + name
            self.send_message(msg, guid)

    def odds(self, guid, number):
        if number < 1:
            msg = "Odds must be with 1 or above"
            self.send_message(msg, guid)

        num1 = random.randint(1, number)
        num2 = random.randint(1, number)
        result = ""
        if num1 == num2:
            result = "I demand completion of the odds!!"
        else:
            result = "no dice."
        msg = "%s and %s - %s" % (num1, num2, result)
        self.send_message(msg, guid)

    def roll(self, guid, number):
        if number < 1:
            msg = "roll must be with 1 or above"
            self.send_message(msg, guid)

        num1 = random.randint(1, number)
        msg = "You rolled a %s" % (num1)
        self.send_message(msg, guid)

    def dog_pic(self, guid):
        self.send_message("Enjoy your dog picture!", guid)
        msg = "https://preview.redd.it/8c1cagvl5sy51.png?width=496&format=png&auto=webp&s=1005c586ec187aeb6ab961e66f69d1bf0a7e91c9"
        self.send_message(msg, guid, noRobot=True)

    def read(self, message):
        global weaponized
        if not message[MESSAGE_CONTENT]:
            pass
        text = message[MESSAGE_CONTENT].text
        date = message[MESSAGE_CONTENT].date
        command = text.split(" ")
        guid = message[GUID]
        print (command)
        if(command[0] == "@Edgar" or command[0] == "@edgar"):
            print (guid)
            command.pop(0)
            command = " ".join(command)

            if re.match(r"are you here.*", command, re.IGNORECASE):
                self.here(guid)
            elif re.match(r"what are you.*", command, re.IGNORECASE):
                self.what_am_i(guid)
            elif re.match(r"remember .*? is .*?", command, re.IGNORECASE):
                string1 = re.search(r"remember (.*?) is", command, re.IGNORECASE).group(1)
                string2 = re.search(r"(.*? is )(.*?)$", command, re.IGNORECASE).group(2)
                self.remember(guid, string1, string2)
            elif re.match(r"what is .*?", command, re.IGNORECASE):
                string1 = re.search(r"what is (.*?)\??$", command, re.IGNORECASE).group(1)
                self.recall(guid, string1)
            elif re.match(r"did you hear( a)? 4.*?", command, re.IGNORECASE):
                msg = ["I heard a 4", "I definitely heard 4, anyone else hear a 4?", "*Beep Boop* Thats a yar darg"]
                self.send_message(random.choice(msg), guid)
            elif re.match(r"odds [0-9]*$", command, re.IGNORECASE):
                number = [int(s) for s in command.split() if s.isdigit()][0]
                self.odds(guid, number)
            elif re.match(r"dog pic.*?", command, re.IGNORECASE):
                self.dog_pic(guid)
            elif re.match(r"song of the week .*?", command, re.IGNORECASE):
                regex = re.search(r"song of the week (.*?)$", command, re.IGNORECASE)
                name = regex.group(1)
                self.get_song(guid, name)
            elif re.match(r"set song of the week (.*?) (.*?)$", command, re.IGNORECASE):
                regex = re.search(r"set song of the week (.*?) (.*?)$", command, re.IGNORECASE)
                song = regex.group(1)
                name = regex.group(2)
                self.set_song(guid, song, name)
            elif re.match(r"good bot.*?|thank you.*?|thanks.*?", command, re.IGNORECASE):
                msg = "Glad I could be of assistance, meatbag. *Beep Boop*"
                self.send_message(msg, guid)
            elif re.match(r"dick pic.*?", command, re.IGNORECASE):
                msg = "Enjoy your dick picture!"
                self.send_message(msg, guid)
                msg = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/46_Dick_Cheney_3x4.jpg/1200px-46_Dick_Cheney_3x4.jpg"
                self.send_message(msg, guid, noRobot=True)
            elif re.match(r"arm the kitten cannon (\d{10})", command, re.IGNORECASE):
                regex = re.search(r"arm the kitten cannon (\d{10})", command, re.IGNORECASE)
                weaponized = regex.group(1)
                msg = "Tater cat weaponized, sir, and aimed at +1%s" % (weaponized)
                self.send_message(msg, guid)
            elif re.match(r"roll \d{1,20}", command, re.IGNORECASE):
                regex = re.search(r"roll (\d{1,20})", command, re.IGNORECASE)
                number = int(regex.group(1))
                self.roll(guid, number)
            elif re.match(r"fire.*?", command, re.IGNORECASE) and weaponized:
                msg = "Locked on target. Commencing launch sequence"
                self.send_message(msg, guid)
                cannon = """
                for ((i=1; i<=100; i++)); do
                osascript -e 'tell application "Messages"
                  set myid to "iMessage;-;+1%s"
                  set ImageAttachment to POSIX file "./ammo.png" as alias
                  set theBuddy to a reference to text chat id myid
                  send ImageAttachment to theBuddy
                end tell'
                done
                """ % (weaponized)
                os.system(cannon)
                weaponized = False


            else:
                self.send_message("I dont recognize that command. Text @Edgar what are you? for help", guid)
