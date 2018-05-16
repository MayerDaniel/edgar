import imessage
import threading
import sys
import time
import os
import logging
import edgarbot
import getpass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    sleep_time = 0.1
    def get_Edgar(self, Edgar):
        self.Edgar = Edgar
    def on_modified(self, event):
        messages = imessage.get_last_message()
        threads = []
        for message in messages:
            t = threading.Thread(target=self.Edgar.read(message))
            threads.append(t)
            t.start()

class Listener:
    def __init__(self):
        self.Ed = edgarbot.Edgar()

    def listen(self):
        print ("Edgar is listening!")
        homedir = os.environ['HOME']
        path = homedir + "/Library/Messages/"
        event_handler = MyHandler()
        event_handler.get_Edgar(self.Ed)
        observer = Observer(timeout=0.5)
        observer.event_queue.maxsize=10
        observer.schedule(event_handler, path, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

def main():
    l = Listener()
    l.listen()

if __name__ == '__main__':
    main()
