import user
import other
import pytest
from error import InputError

def test_user_profile():
	# Function user_profile(token, u_id)
	# Returns {user}
	# For a valid user, returns information about their email, first name, last name, and handle

def test_user_profile_except():
	# InputError:
	#	User with u_id is not a valid user

def test_user_profile_setname():
	# Function user_profile(token, name_first, name_last)
	# Returns {}
	# Update the authorised user's first and last name

def test_user_profile_setname_except():
	# InputError:
	#	name_first is not between 1 and 50 characters in length
	#	name_last is not between 1 and 50 characters in length

def test_user_profile_setemail():
	# Function user_profile(token, email)
	# Returns {}
	# Update the authorised user's email address

def test_user_profile_setemail_except():
	# InputError:
	#	Email entered is not a valid email
	#	Email address is already being used by another user

def test_user_profile_sethandle():
	# Function user_profile(token, handle_str)
	# Returns {}
	# Update the authorised user's handle (i.e. display name)

def test_user_profile_sethandle_except():
	# InputError:
	#	handle_str must be between 3 and 20 characters
	#	handle is already used by another user

def test_users_all():
	# Function users_all(token)
	# Returns {users}
	# No description given

def search():
	# Function search(token, query_str)
	# Returns {messages}
	# Given a query string, return a collection of messages in all of the channels that the user has joined that match the query