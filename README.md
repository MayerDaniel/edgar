# edgarbot
&lt;I^_^|> *Beep Boop*

edgarbot is a chatbot that lives in your imessages!

Inspired by hubot, Edgar is a work in progress that aims to be a programmable chatbot which you and all of your friends can talk to when using imessage.

Edgar works by linking together various bits of information/functionality on your OSX machine:

- The sqlite DBs that contain all of your imessage data
- ~~Your contacts from your icloud account~~ NO LONGER!!
- Applescript's ability to communicate with native apps

Edgar is very much a work in progress but can run on your very own iMessage instance!
- Clone this repo
- run "python3 start_edgar.py"
- Sent a text to someone saying "@Edgar are you here?"
- For a full list of commands, text someone "@Edgar what are you?"

Libraries that were used as references:

https://github.com/mattrajca/pymessage-lite

# TODO:

- Create Method for implementing new command and regex
  - Create pickled command datastructure for persistent user commands
- ~~Figure out where group chat handles are stored in the SQLite DB and how to implement sending them with applescript~~ DONE
- Implement changeable name (but he will always be Edgar in my heart)
- Catch if multiple people in same chat have edgars, have only one respond to commands.
- ~~Replicate 'unknown chat' bug that occurs every once in a while...~~ SEEMS TO BE FIXED WITH SWITCH TO PYTHON3
