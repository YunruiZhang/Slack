import auth
import pytest
from error import InputError, AccessError


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
	result = auth.auth_register('yunrui1.zhang@studnet.unsw.edu.au','123456','Yunrui','Zhang')
	with pytest.raises(InputError) as e:
		auth.auth_login('yunrui1.zhang@student.unsw.edu.au','123456789')
	#not registered email
	with pytest.raises(InputError) as e:
		auth.auth_login('yunrui1.zhang123@student.unsw.edu.au','123456')
	# InputError:
	#	Email entered is not a valid email 
	#	Email entered does not belong to a user
	#	Password is incorrect
	
	
def test_auth_logout():
	#Try normal logout 
	result = auth.auth_register('yunrui2.zhang@studnet.unsw.edu.au','123456','Yunrui','Zhang')
	result1 = auth.auth_logout(result['token'])
	token1 = result1['is_success']
	assert token1 == True
	# Try double logout
	result2 = auth.auth_logout(result['token'])
	token2 = result2['is_success']
	assert token2 == False
	#Try to pass a invalid token
	#assert auth.auth_logout(123) == False

	# Function auth_logout(token)
	# Returns {is_success}
	# Given an active token, invalidates the taken to log the user out. If a valid token is given, and the user is successfully logged out, it returns true, otherwise false.


def test_auth_register():
	result = auth.auth_register('yunrui3.zhang@studnet.unsw.edu.au','123456','Yunrui','Zhang')
	# Function auth_register(email,password,name_first,name_last)
	# Returns {u_id,token}
	# Given a user's first and last name, email address, and password, create a new account for them and return a new token for authentication in their session. A handle is generated that is the concatentation of a lowercase-only first name and last name. If the concatenation is longer than 20 characters, it is cutoff at 20 characters. If the handle is already taken, you may modify the handle in any way you see fit to make it unique.


def test_auth_register_except():
	#short password
	with pytest.raises(InputError) as e:
		auth.auth_register('yunrui4.zhang@studnet.unsw.edu.au','12345','Yunrui','Zhang')
	#Invalid email
	with pytest.raises(InputError) as e:
		auth.auth_register('i hate python','12345','Yunrui','Zhang')
	#double register
	result = auth.auth_register('yunrui5.zhang1@studnet.unsw.edu.au','123456','Yunrui','Zhang')
	with pytest.raises(InputError) as e:
		auth.auth_register('yunrui5.zhang1@studnet.unsw.edu.au','123456','Yunrui','Zhang')
	#short first name
	with pytest.raises(InputError) as e:
		auth.auth_register('yunrui6.zhang2@studnet.unsw.edu.au','123456','','Zhang')
	#long first name
	with pytest.raises(InputError) as e:
		auth.auth_register('yunrui7.zhang3@studnet.unsw.edu.au','123456','y'*51,'Zhang')
	#short last name
	with pytest.raises(InputError) as e:
		auth.auth_register('yunrui8.zhang4@studnet.unsw.edu.au','123456','Yunrui','')
	#long last name
	with pytest.raises(InputError) as e:
		auth.auth_register('yunrui9.zhang5@studnet.unsw.edu.au','123456','Yunrui','z'*51)
	#	Email entered is not a valid email 
	#	Email address is already being used by another user
	#	Password entered is less than 6 characters long
	#	name_first not is between 1 and 50 characters in length
	#	name_last is not between 1 and 50 characters in length
