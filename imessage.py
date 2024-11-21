from os.path import expanduser
import sqlite3
import datetime
import typedstream
import re

OSX_EPOCH = 978307200
LAST_READ = -1

# Represents a user that iMessages can be exchanged with.
#
# Each user has...
#  - an `id` property that uniquely identifies him or her in the Messages database
#  - a `phone_or_email` property that is either the user's phone number or iMessage-enabled email address
class Recipient:
	def __init__(self, id, phone_or_email):
		self.id = id
		self.phone_or_email = phone_or_email

	def __repr__(self):
		return "ID: " + str(self.id) + " Phone or email: " + self.phone_or_email

# Represents an iMessage message.
#
# Each message has:
#  - a `text` property that holds the text contents of the message
#  - a `date` property that holds the delivery date of the message
class Message:
	def __init__(self, text, date):
		self.text = text.decode()
		self.date = date

	def __repr__(self):
		return "Text: " + self.text + " Date: " + str(self.date)

def _new_connection():
    # The current logged-in user's Messages sqlite database is found at:
    # ~/Library/Messages/chat.db
	db_path = expanduser("~") + '/Library/Messages/chat.db'
	return sqlite3.connect(db_path)


def id_to_guid(row_id):
	connection = _new_connection()
	c = connection.cursor()

    # The `message` table stores all exchanged iMessages.
	chat = ''
	while chat == '':
		c.execute("SELECT * FROM chat_message_join WHERE message_id=" + str(row_id))
		for row in c:
			# print(row)
			chat = row[0]
	guid = []
	print("CHAT = " + str(chat))
	c.execute("SELECT * FROM chat WHERE ROWID=" + str(chat))
	for row in c:
		guid.append(str(row[1]))
	return guid[0]


# Fetches all messages exchanged with a given recipient.
def get_last_message():
	global LAST_READ

	connection = _new_connection()
	c = connection.cursor()
    # The `message` table stores all exchanged iMessages.
	text = ''
	row_id = ''
	date = ''
	if LAST_READ == -1:
		c.execute("SELECT * FROM message WHERE ROWID = (SELECT MAX(ROWID) FROM message)")
	else:
		c.execute("SELECT * FROM message WHERE ROWID > " + str(LAST_READ))

	messages = []
	for row in c:
		row_id = row[0]
		
		#sometime messages are in row 2 and sometimes they are in an NSData object in row 8
		text = row[2]

		if text is None:
			data = row[8]
			print(data)
			# print type of textstream
			ts = typedstream.unarchive_from_data(data)
			# print all functions and properties of the textstream
			
			for c in ts.contents:
				for v in c.values:
					# check if v has the property 'archived_name'
					if not (hasattr(v, 'archived_name') and hasattr(v, 'value')):
						continue

					if v.archived_name == b'NSMutableString':
						text = v.value
						break

		if text is None:
			continue

		print(row[15])
		date = datetime.datetime.now()
		encoded_text = text.encode('ascii', 'ignore')
		message = Message(encoded_text, date)
		guid = id_to_guid(row_id)
		LAST_READ = row_id
		messages.append([message, guid])

	return(messages)


	connection.close()

print(get_last_message())
