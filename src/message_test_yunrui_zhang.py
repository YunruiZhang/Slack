import message
import pytest
import channel
import channels
import auth
import database
from error import InputError, AccessError

def test_message_send():
	#get a user
	result = get_user("user1")
	u_id = result['u_id']
	token = result['token']
	#get a channel
	channel = channels.channels_create(token, "channel1", True)
	#send the message
	msgid = message.message_send(token, channel['channel_id'], "hello")
	# Function message_send(token, channel_id, message)
	# Returns {message_id}
	# Send a message from authorised_user to the channel specified by channel_id
	#database.reset()
def test_message_send_except():
	database.reset()
	#long message
	result = get_user("user1")
	u_id = result['u_id']
	token = result['token']
	channel = channels.channels_create(token, "channel1", True)
	with pytest.raises(InputError) as e:
		message.message_send(token, channel['channel_id'], 'a'*1001)
	#try to send a message with a user not in the channel
	result = get_user("user2")
	u_id = result['u_id']
	token = result['token']
	with pytest.raises(AccessError) as e:
		message.message_send(token, channel['channel_id'], "hello")

	# InputError:
	#	Message is more than 1000 characters
	# AccessError:
	#	The authorised user has not joined the channel they are trying to post to

def test_message_remove():
	#create a message
	database.reset()
	result = get_user("user1")
	u_id = result['u_id']
	token = result['token']
	channel_result = channels.channels_create(token, "channel1", True)
	msgid1 = message.message_send(token, channel_result['channel_id'], "hello")
	msg1 = msgid1['message_id']
	#remove the message
	message.message_remove(token, msg1)
	#have a new user and join the channel
	result = get_user("user2")
	u_id1 = result['u_id']
	token1 = result['token']
	channel.channel_join(token1, channel_result['channel_id'])
	#new user send a message
	msgid2 = message.message_send(token1, channel_result['channel_id'], "hello")
	msg2 = msgid2['message_id']
	#admin remove the new message
	message.message_remove(token, msg2)
	#new user send another message
	msgid3 = message.message_send(token1, channel_result['channel_id'], "wow")
	#new user remove the message
	message.message_remove(token1, msgid3['message_id'])
	# Function message_remove(token, message_id)
	# Returns {}
	# Given a message_id for a message, this message is removed from the channel

def test_message_remove_except():
	database.reset()
	#create a message and remove it
	result = get_user("user1")
	u_id = result['u_id']
	token = result['token']
	temp = channels.channels_create(token, "channel1", True)
	channel_id = temp['channel_id']
	msg = message.message_send(token, channel_id, "hello")
	message.message_remove(token, msg['message_id'])
	#try to remove it again
	with pytest.raises(InputError) as e:
		message.message_remove(token, msg['message_id'])
	#create the same message again
	msg = message.message_send(token, channel_id, "hello")
	#create a new user and join the channel and use the new user's token to remove the message
	result = get_user("user2")
	u_id = result['u_id']
	token = result['token']
	channel.channel_join(token, channel_id)
	with pytest.raises(AccessError) as e:
		message.message_remove(token, msg['message_id'])
	# InputError:
	#	Message (based on ID) no longer exists
	# AccessError (When none of the following are true):
	#	Message with message_id was sent by the authorised user making this request
	#	The authorised user is an admin or owner of this channel or the slackr

def test_message_edit():
	database.reset()
	#send a message
	result = get_user("user1")
	u_id = result['u_id']
	token = result['token']
	temp = channels.channels_create(token, "channel1", True)
	channel_id = temp['channel_id']
	msg = message.message_send(token, channel_id, "hello")
	message_id = msg['message_id']
	#edit the message
	return_val = message.message_edit(token, message_id, "hi")
	assert return_val == {}
	#edit the message to an empty string so the message is deleted
	message.message_edit(token, message_id, "")
	#try to delete the message which is deleted
	with pytest.raises(InputError) as e:
		message.message_remove(token, message_id)
	#have a new user join the channel and send a message
	result = get_user("user2")
	u_id2 = result['u_id']
	token2 = result['token']
	channel.channel_join(token2, channel_id)
	msg2 = message.message_send(token2, channel_id, "hello")
	#admin edit the new message
	temp2 = message.message_edit(token, msg2['message_id'], "hi")
	assert temp2 == {}
	#new user edit him message
	temp3 = message.message_edit(token2, msg2['message_id'], "hillo")
	assert temp3 == {}
	# Function message_remove(token, message_id, message)
	# Returns {}
	# Given a message, update it's text with new text. If the new message is an empty string, the message is deleted.

def test_message_edit_except():
	#send a message
	database.reset()
	result = get_user("user1")
	u_id = result['u_id']
	token = result['token']
	temp = channels.channels_create(token, "channel1", True)
	channel_id = temp['channel_id']
	temp1 = message.message_send(token, channel_id, "hello")
	msg_id = temp1['message_id']
	#create a new user and join the channel
	result = get_user("user2")
	u_id2 = result['u_id']
	token2 = result['token']
	channel.channel_join(token2, channel_id)
	# try to use new user's token to edit the message
	with pytest.raises(AccessError) as e:
		message.message_edit(token2, msg_id, "hi")
	# try to edit the message to more than 1000 characters
	with pytest.raises(InputError) as e:
		message.message_edit(token, msg_id, 'h'*1001)
	# AccessError (When none of the following are true):
	#	Message with message_id was sent by the authorised user making this request	
	#	The authorised user is an admin or owner of this channel or the slackr

def get_user(username):
	#register a user and return u_id and token
    return auth.auth_register(username+"@gmail.com", "password123", "Edward", "ZHANG")