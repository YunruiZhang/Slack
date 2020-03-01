import auth
import pytest
from error import InputError

def test_auth_login():
	# Function auth_login(email,password)
	# Returns {u_id, token}
	# Given a registered users' email and password and generates a valid token for the user to remain authenticated

def test_auth_login_except():
	# InputError:
	#	Email entered is not a valid email 
	#	Email entered does not belong to a user
	#	Password is incorrect

def test_auth_logout():
	# Function auth_logout(token)
	# Returns {is_success}
	# Given an active token, invalidates the taken to log the user out. If a valid token is given, and the user is successfully logged out, it returns true, otherwise false.

def test_auth_register():
	# Function auth_register(email,password,name_first,name_last)
	# Returns {u_id,token}
	# Given a user's first and last name, email address, and password, create a new account for them and return a new token for authentication in their session. A handle is generated that is the concatentation of a lowercase-only first name and last name. If the concatenation is longer than 20 characters, it is cutoff at 20 characters. If the handle is already taken, you may modify the handle in any way you see fit to make it unique.

def test_auth_refister_except():
	# InputError:
	#	Email entered is not a valid email 
	#	Email address is already being used by another user
	#	Password entered is less than 6 characters long
	#	name_first not is between 1 and 50 characters in length
	#	name_last is not between 1 and 50 characters in length