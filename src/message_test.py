import message
import pytest
from error import InputError

def test_message_send():
	# Function message_send(token, channel_id, message)
	# Returns {message_id}
	# Send a message from authorised_user to the channel specified by channel_id

def test_message_send_except():
	# InputError:
	#	Message is more than 1000 characters
	# AccessError:
	#	The authorised user has not joined the channel they are trying to post to

def test_message_remove():
	# Function message_remove(token, message_id)
	# Returns {}
	# Given a message_id for a message, this message is removed from the channel

def test_message_remove_except():
	# InputError:
	#	Message (based on ID) no longer exists
	# AccessError (When none of the following are true):
	#	Message with message_id was sent by the authorised user making this request
	#	The authorised user is an admin or owner of this channel or the slackr

def test_message_edit():
	# Function message_remove(token, message_id, message)
	# Returns {}
	# Given a message, update it's text with new text. If the new message is an empty string, the message is deleted.

def test_message_edit_except():
	# AccessError (When none of the following are true):
	#	Message with message_id was sent by the authorised user making this request	
	#	The authorised user is an admin or owner of this channel or the slackr
