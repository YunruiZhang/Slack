from message import*
from auth import * 
from channels import *
from channel import channel_invite, channel_messages
import pytest
from error import InputError, AccessError

#set up
owner = auth_register('owner@gmail.com', 'qwertyui8', 'ownerF', 'ownerL')
owner_id = owner['u_id']
owner_token = owner['token']
owner_handle = 'ownerF'+'ownerL'

member = auth_register('member@gmail.com', 'qwertyui8', 'memberF', 'memberL')
member_id = member['u_id']
member_token = member['token']
member_handle = 'memberF'+'memberL'

#each person create a channel on their own 
c_id1 = channels_create(owner_token, 'channel_1', True)['channel_id']
c_id2 = channels_create(member_token, 'channel_2', False)['channel_id']

#both owner and member are now in channel 1
channel_invite(owner_token, c_id1, member_id)

#owner sends 2 messages to channel_1, which was created by onwer
m_id1 = message_send(owner_token, c_id1, 'first message in channel 1')['message_id']
m_id2 = message_send(owner_token, c_id1, 'second message in channel 1')['message_id']

new_mes = 'making changes'


def test_message_send():
	# Function message_send(token, channel_id, message)
	# Returns {message_id}
	# Send a message from authorised_user to the channel specified by channel_id
	assert(m_id1 > 0)


def test_message_send_except():
	# InputError:
	#	Message is more than 1000 characters
	with pytest.raises(InputError):
		message_send(owner_token, c_id1, 'long'*250+'l')

	# AccessError:
	#	The authorised user has not joined the channel they are trying to post to
	with pytest.raises(AccessError):
		message_send(owner_token, c_id2, 'legal message')

	

def test_message_remove():
	# Function message_remove(token, message_id)
	# Returns {}
	# Given a message_id for a message, this message is removed from the channel
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 2
	message_remove(owner_token, m_id1)
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 1

def test_message_remove_except():
	# InputError:
	#	Message (based on ID) no longer exists
	with pytest.raises(InputError):
		message_remove(owner_token, 300)

	# AccessError (When none of the following are true):
	#	Message with message_id was sent by the authorised user making this request
	#	The authorised user is an admin or owner of this channel or the slackr
	with pytest.raises(AccessError):
		message_remove(member_token, m_id2) # fail

def test_message_edit():
	# Function message_remove(token, message_id, message)
	# Returns {}
	# Given a message, update it's text with new text. 
	message_edit(owner_token, m_id2, new_mes) # with m_id1 removed before, only m_id2 in the channel_1
	assert channel_messages(owner_token, c_id1, 0)['messages'][0]['message'] == new_mes
	
	#If the new message is an empty string, the message is deleted.
	len(channel_messages(owner_token, c_id1, 0)['messages']) == 1
	message_edit(owner_token, m_id2, '')
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 0


def test_message_edit_except():
	# AccessError (When none of the following are true):
	#	Message with message_id was sent by the authorised user making this request	
	#	The authorised user is an admin or owner of this channel or the slackr
	with pytest.raises(AccessError):
		message_edit(member_token, m_id2, new_mes)
		