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

channel_invite(owner_token, c_id1, member_id) #both owner and member are now in channel 1

m_id1 = message_send(owner_token, c_id1, 'first message in channel 1')['message_id']
m_id2 = message_send(owner_token, c_id1, 'second message in channel 1')['message_id']
m_id3 = message_send(member_token, c_id1, 'third message in channel 1')['message_id'] # the 3rd msg in ch_1 sent by member
m_id4 = message_send(member_token, c_id1, 'fourth message in channel 1')['message_id'] # the 4th msg in ch_1 sent by member

new_mes = 'making changes'


def test_message_send():
	# Function message_send(token, channel_id, message)
	# Returns {message_id}
	# Send a message from authorised_user to the channel specified by channel_id
	
	# by owner
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 4
	msgowner_id = message_send(owner_token, c_id1, 'sent by owner')['message_id']
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 5
	message_remove(owner_token, msgowner_id)

	# by member 
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 4
	msgmember_id = message_send(member_token, c_id1, 'sent by member')['message_id']
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 5
	message_remove(member_token, msgmember_id)

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
	
	# test for owner delete message sent by owner
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 4
	message_remove(owner_token, m_id1)
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 3

	# test for owner delete message sent by member
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 3
	message_remove(owner_token, m_id3)
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 2

	# test for member delete message sent by member
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 2
	message_remove(member_token, m_id4)
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 1
	
	#leaving only m_id2

def test_message_remove_except():
	# InputError:
	#	Message (based on ID) no longer exists
	with pytest.raises(InputError):
		message_remove(owner_token, m_id1)

	# AccessError (When none of the following are true):
	#	Message with message_id was sent by the authorised user making this request
	#	The authorised user is an admin or owner of this channel or the slackr
	
	# member delete msg sent by owner
	with pytest.raises(AccessError):
		message_remove(member_token, m_id2) 

def test_message_edit():
	# Function message_remove(token, message_id, message)
	# Returns {}

	# owner edit owner's message
	# Given a message, update it's text with new text. 
	message_edit(owner_token, m_id2, new_mes) # with m_id1 removed before, only m_id2 in the channel_1
	assert channel_messages(owner_token, c_id1, 0)['messages'][0]['message'] == new_mes
	#If the new message is an empty string, the message is deleted.
	len(channel_messages(owner_token, c_id1, 0)['messages']) == 1
	message_edit(owner_token, m_id2, '')
	assert len(channel_messages(owner_token, c_id1, 0)['messages']) == 0
	#try to delete the message which is deleted, which will send an error
	with pytest.raises(InputError) :
		message_remove(owner_token, m_id2)

	# owner edit member's msg
	m_id5 = message_send(member_token, c_id1, 'fifth message in channel 1')['message_id']
	message_edit(owner_token, m_id5, new_mes)
	assert channel_messages(owner_token, c_id1, 0)['messages'][0]['message'] == new_mes

def test_message_edit_except():
	# AccessError (When none of the following are true):
	#	Message with message_id was sent by the authorised user making this request	
	#	The authorised user is an admin or owner of this channel or the slackr
	with pytest.raises(AccessError):
		message_edit(member_token, m_id2, new_mes)
	# member edit member's message but too long
	m_id6 = message_send(member_token, c_id1, 'sixth message in channel 1')['message_id']
	with pytest.raises(InputError):
		message_edit(member_token, m_id6, 'h'*1001)
		