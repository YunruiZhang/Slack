import auth
import pytest
from error import InputError

def test_auth_login():
	result = auth.auth_register('yunrui.zhang@studnet.unsw.edu.au','123456','Yunrui','Zhang')
	result1 = auth.auth_login('yunrui.zhang@studnet.unsw.edu.au','123456')
	# Function auth_login(email,password)
	# Returns {u_id, token}
	# Given a registered users' email and password and generates a valid token for the user to remain authenticated

def test_auth_login_except():
	#test for invalid email
	with pytest.raises(InputError) as e:
		auth.auth_login('1122','123456')
	#incorrect password
	result = auth.auth_register('yunrui.zhang@studnet.unsw.edu.au','123456','Yunrui','Zhang')
	with pytest.raises(InputError) as e:
		auth.auth_login('yunrui.zhang@student.unsw.edu.au','123456789')
	#not registered email
	with pytest.raises(InputError) as e:
		auth.auth_login('yunrui.zhang123@student.unsw.edu.au','123456')
	# InputError:
	#	Email entered is not a valid email 
	#	Email entered does not belong to a user
	#	Password is incorrect

def test_auth_logout():
	#Try normal logout 
	result = auth.auth_register('yunrui.zhang@studnet.unsw.edu.au','123456','Yunrui','Zhang')
	assert auth.auth_logout(result) == True
	# Try double logout
	assert auth.auth_logout(result) == False
	#Try to pass a invalid token
	assert auth.auth_logout(123) == False

	# Function auth_logout(token)
	# Returns {is_success}
	# Given an active token, invalidates the taken to log the user out. If a valid token is given, and the user is successfully logged out, it returns true, otherwise false.

def test_auth_register():
	result = auth.auth_register('yunrui.zhang@studnet.unsw.edu.au','123456','Yunrui','Zhang')
	# Function auth_register(email,password,name_first,name_last)
	# Returns {u_id,token}
	# Given a user's first and last name, email address, and password, create a new account for them and return a new token for authentication in their session. A handle is generated that is the concatentation of a lowercase-only first name and last name. If the concatenation is longer than 20 characters, it is cutoff at 20 characters. If the handle is already taken, you may modify the handle in any way you see fit to make it unique.



def test_auth_refister_except():
	#short password
	with pytest.raises(InputError) as e:
		auth.auth_register('yunrui.zhang@studnet.unsw.edu.au','12345','Yunrui','Zhang')
	#Invalid email
	with pytest.raises(InputError) as e:
		auth.auth_register('i hate python','12345','Yunrui','Zhang')
	#double register
	result = auth.auth_register('yunrui.zhang1@studnet.unsw.edu.au','123456','Yunrui','Zhang')
	with pytest.raises(InputError) as e:
		auth.auth_register('yunrui.zhang1@studnet.unsw.edu.au','123456','Yunrui','Zhang')
	#short first name
	with pytest.raises(InputError) as e:
		auth.auth_register('yunrui.zhang2@studnet.unsw.edu.au','123456','','Zhang')
	#long first name
	with pytest.raises(InputError) as e:
		auth.auth_register('yunrui.zhang3@studnet.unsw.edu.au','123456','y'*51,'Zhang')
	#short last name
	with pytest.raises(InputError) as e:
		auth.auth_register('yunrui.zhang4@studnet.unsw.edu.au','123456','Yunrui','')
	#long last name
	with pytest.raises(InputError) as e:
		auth.auth_register('yunrui.zhang5@studnet.unsw.edu.au','123456','Yunrui','z'*51)
	#	Email entered is not a valid email 
	#	Email address is already being used by another user
	#	Password entered is less than 6 characters long
	#	name_first not is between 1 and 50 characters in length
	#	name_last is not between 1 and 50 characters in length