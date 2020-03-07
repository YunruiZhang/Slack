import user
import other
from user import *
from other import * 
from auth import * 
from channels import *
from channel import *
from message import message_send
import pytest
from error import InputError

# set up users 
owner = auth_register('owner@gmail.com', 'qwertyui8', 'ownerF', 'ownerL')
owner_id = owner['u_id']
owner_token = owner['token']
owner_handle = 'ownerF'+'ownerL'

member = auth_register('member@gmail.com', 'qwertyui8', 'memberF', 'memberL')
member_id = member['u_id']
member_token = member['token']
member_handle = 'memberF'+'memberL'


def test_user_profile():
	# Function user_profile(token, u_id)
	# Returns {user}
	# For a valid user, returns information about their email, first name, last name, and handle
	user_1 = user_profile(owner_token, owner_id)
	assert(user_1['email'] == 'owner@gmail.com')
	assert(user_1['name_first'] == 'ownerF')
	assert(user_1['name_last'] == 'ownerL')
	assert(user_1['handle_str'] == owner_handle)


def test_user_profile_except():
	# InputError:
	#	User with u_id is not a valid user
	with pytest.raises(InputError):
		user_profile(owner_token, 123456789)


def test_user_profile_setname():
	# Function user_profile(token, name_first, name_last)
	# Returns {}
	# Update the authorised user's first and last name
	user_profile_setname(owner_token, 'newownerF', 'newownerL')
	user_2 = user_profile(owner_token, owner_id)
	assert(user_2['name_first'] == 'newownerF')
	assert(user_2['name_last'] == 'newownerL')


def test_user_profile_setname_except():
	# InputError:
	#	name_first is not between 1 and 50 characters in length
	with pytest.raises(InputError):
		user_profile_setname(owner_token, 'badfirstname'*10, 'newownerL')

	#	name_last is not between 1 and 50 characters in length
	with pytest.raises(InputError):
		user_profile_setname(owner_token, 'newownerF', 'badlastname'*10)

def test_user_profile_setemail():
	# Function user_profile(token, email)
	# Returns {}
	# Update the authorised user's email address
	user_profile_setemail(owner_token, 'newowner@gmail.com')
	user_3 = user_profile(owner_token, owner_id)
	assert(user_3['email'] == 'newowner@gmail.com')

def test_user_profile_setemail_except():
	# InputError:
	#	Email entered is not a valid email
	with pytest.raises(InputError):
		user_profile_setemail(owner_token, 'a')
	
	#	Email address is already being used by another user
	with pytest.raises(InputError):
		user_profile_setemail(owner_token, 'member@gmail.com')

def test_user_profile_sethandle():
	# Function user_profile(token, handle_str)
	# Returns {}
	# Update the authorised user's handle (i.e. display name)
	user_profile_sethandle(owner_token, 'newowner_handle')
	user_4 = user_profile(owner_token, owner_id)
	assert(user_4['handle_str'] == 'newowner_handle')

def test_user_profile_sethandle_except():
	# InputError:
	#	handle_str must be between 3 and 20 characters
	with pytest.raises(InputError):
		user_profile_sethandle(owner_token, 'h'*2)
	with pytest.raises(InputError):
		user_profile_sethandle(owner_token, 'h'*21)

	#	handle is already used by another user
	with pytest.raises(InputError):
		user_profile_sethandle(owner_token, member_handle)


def test_users_all():
	# Function users_all(token)
	# Returns {users}
	# No description given
	assert(len(users_all(owner_token)) == 2)


def search():
	# Function search(token, query_str)
	# Returns {messages}
	# Given a query string, return a collection of messages in all of the channels that the user has joined that match the query
	# Given a query string, return a collection of messages in all of the channels that the user has joined that match the query
	c_id1 = channels_create(owner_token, 'channel_1', True)['channel_id']
	c_id2 = channels_create(owner_token, 'channel_2', True)['channel_id']
	message_send(owner_token, c_id1, 'first message in channel 1')
	message_send(owner_token, c_id1, 'second message in channel 1')
	message_send(owner_token, c_id2, 'first message in channel 2')
	message_send(owner_token, c_id2, 'second message in channel 2')
	assert(len(search('first')) == 2)
	assert(len(search('second')) == 2)
	assert(len(search('message')) == 4)
	assert(len(search('others')) == 0)
	
