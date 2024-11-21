import imessage
import threading
import sys
import time
import os
import logging
import edgarbot
import getpass

class Listener:
    def __init__(self):
        self.Ed = edgarbot.Edgar()

    def listen(self):
        print ("Edgar is listening!")
        while True:
            time.sleep(1)
            messages = imessage.get_last_message()
            threads = []
            for message in messages:
                t = threading.Thread(target=self.Ed.read(message))
                threads.append(t)
                t.start()

def main():
    l = Listener()
    l.listen()

if __name__ == '__main__':
    main()
