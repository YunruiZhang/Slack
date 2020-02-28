import channel
import channels
import pytest
from error import InputError

def test_channel_invite():
	# Function channel_invite(token, channel_id, u_id)
	# Returns {}
	# Invites a user (with user id u_id) to join a channel with ID channel_id. Once invited the user is added to the channel immediately

def test_channel_invite_except():
	# InputError:
	#	channel_id does not refer to a valid channel that the authorised user is part of.
	#	u_id does not refer to a valid user
	# Access Error:
	#	The authorised user is not already a member of the channel

def test_channel_details():
	# Function channel_invite(token, channel_id)
	# Returns {name, owner_members, all_members}
	# Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel

def test_channel_details_except():
	# InputError:
	#	Channel ID is not a valid channel
	# Access Error:
	#	Authorised user is not a member of channel with channel_id

def test_channel_messages():
	# Function channel_messages(token, channel_id, start)
	# Returns {messages, start, end}
	# Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.

def test_channel_messages_except():
	# InputError:
	#	Channel ID is not a valid channel
	#	Start is greater than the total number of messages in the channel
	# Access Error:
	#	Authorised user is not a member of channel with channel_id

def test_channel_leave():
	# Function channel_leave(token, channel_id)
	# Returns {}
	# Given a channel ID, the user removed as a member of this channel

def test_channel_leave_except():
	# InputError:
	#	Channel ID is not a valid channel
	# Access Error:
	#	Authorised user is not a member of channel with channel_id

def test_channel_join():
	# Function channel_join(token, channel_id)
	# Returns {}
	# Given a channel_id of a channel that the authorised user can join, adds them to that channel

def test_channel_join_except():
	# InputError:
	#	Channel ID is not a valid channel
	# Access Error:
	#	channel_id refers to a channel that is private (when the authorised user is not an admin)

def test_channel_addowner():
	# Function channel_addowner(token, channel_id, u_id)
	# Returns {}
	# Make user with user id u_id an owner of this channel

def test_channel_addowner_except():
	# InputError:
	#	Channel ID is not a valid channel
	#	When user with user id u_id is already an owner of the channel
	# Access Error:
	#	The authorised user is not an owner of the slackr, or an owner of this channel

def test_channel_removeowner():
	# Function channel_addowner(token, channel_id, u_id)
	# Returns {}
	# Remove user with user id u_id an owner of this channel

def test_channel_removeowner_except():
	# InputError:
	#	Channel ID is not a valid channel
	#	When user with user id u_id is already an owner of the channel
	# Access Error:
	#	The authorised user is not an owner of the slackr, or an owner of this channel

def test_channels_list():
	# Function channels_list(token)
	# Returns {channels}
	# Provide a list of all channels (and their associated details) that the authorised user is part of

def test_channels_listall():
	# Function channels_listall(token)
	# Returns {channels}
	# Provide a list of all channels (and their associated details)

def test_channels_create():
	# Function channels_create(token, name, is_public)	
	# Returns {channel_id}
	# Creates a new channel with that name that is either a public or private channel

def test_channels_create_except():
	# InputError:
	#	Name is more than 20 characters long