import message
import pytest
import channel
import channels
from error import InputError

def test_message_send():
	#get a user
	u_id, token = get_user("user1")
	#get a channel
	channel_id1 = channels.channels_create(token, "channel1", True)
	#join the channel
	channel.channel_join(token, channel_id1)
	#send the message
	msgid = message.message_send(token, channel_id1, "hello")
	# Function message_send(token, channel_id, message)
	# Returns {message_id}
	# Send a message from authorised_user to the channel specified by channel_id

def test_message_send_except():
	#long message
	u_id, token = get_user("user1")
	channel_id1 = channels.channels_create(token, "channel1", True)
	channel.channel_join(token, channel_id1)
	with pytest.raises(InputError) as e:
		message.message_send(token, channel_id1, 'a'*1001)
	#not joined the channel
	u_id2, token2 = get_user("user2")
	with pytest.raises(AccessError) as e:
		message.message_send(token2, channel_id1, "hello")

	# InputError:
	#	Message is more than 1000 characters
	# AccessError:
	#	The authorised user has not joined the channel they are trying to post to

def test_message_remove():
	#create a message
	u_id, token = get_user("user1")
	channel_id1 = channels.channels_create(token, "channel1", True)
	channel.channel_join(token, channel_id1)
	msgid = message.message_send(token, channel_id1, "hello")
	#remove the message
	message.message_remove(token, msgid)
	# Function message_remove(token, message_id)
	# Returns {}
	# Given a message_id for a message, this message is removed from the channel

def test_message_remove_except():
	#create a message and remove it
	u_id, token = get_user("user1")
	channel_id1 = channels.channels_create(token, "channel1", True)
	channel.channel_join(token, channel_id1)
	msgid = message.message_send(token, channel_id1, "hello")
	message.message_remove(token, msgid)
	#try to remove it again
	with pytest.raises(InputError) as e:
		message.message_remove(token, msgid)
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

def get_user(username):
	#register a user and return u_id and token
    return auth.auth_register(username+"@gmail.com", "password123", "Edward", "ZHANG")