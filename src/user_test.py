import other,auth,message,channel,channels,user
import pytest
from error import InputError,AccessError
import re

token = 123456
u_id = 1
name_first = 'Python'
name_last = 'Forever'
email = '123456@unsw.edu.au'
handle_str = 'sbocajh'

# Make a regular expression 
# for validating an Email 
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
      
# Define a function for 
# for validating an Email 
def check(email):  
    if(re.search(regex,email)):  
        return("Valid Email")  
          
    else:  
        return("Invalid Email") 


#---------------------------------test invalid u_id--------------------------------------------#
def test_invalid_u_id():
    person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_token = login_person1['token']
    with pytest.raises(InputError) as e:
        assert user.user_profile(person1_token, 10002)



#---------------------------------test invalid user's name--------------------------------------------#
def test_invalid_name_first_long():
    #person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_token = login_person1['token']
    with pytest.raises(InputError) as e:
        assert user.user_profile_setname(person1_token, 'a'*52, 'Forever')

def test_invalid_name_first_short():
    #person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_token = login_person1['token']
    with pytest.raises(InputError) as e:
        assert user.user_profile_setname(person1_token, '', 'Forever')

def test_invalid_name_last_long():
   # person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_token = login_person1['token']
    with pytest.raises(InputError) as e:
        assert user.user_profile_setname(person1_token, 'Python', 'a'*52)

def test_invalid_name_last_short():
   # person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_token = login_person1['token']
    with pytest.raises(InputError) as e:
        assert user.user_profile_setname(person1_token, 'Python', '')




#---------------------------------test invalid user's email--------------------------------------------#        
def test_invalid_used_email():
   # person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    person2 = auth.auth_register('cs1532@cse.unsw.edu.au', 'abc1234', 'Marry', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_token = login_person1['token']
    with pytest.raises(InputError) as e:
        assert user.user_profile_sethandle(person1_token, 'cs1532@cse.unsw.edu.au')

def test_invalid_email():
  #  person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_token = login_person1['token']
    #if check('123.com') != "Valid Email":
  #      raise Exception(error.InputError)
    with pytest.raises(InputError) as e:
        assert user.user_profile_setemail(person1_token,'123.com')


#---------------------------------test invalid user's handle-------------------------------------------#
def test_invalid_handle_long():
   # person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_token = login_person1['token']
    with pytest.raises(InputError) as e:
        assert user.user_profile_sethandle(person1_token, 'a'*21)
        
def test_invalid_handle_short():
   # person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_token = login_person1['token']
    with pytest.raises(InputError) as e:
        assert user.user_profile_sethandle(person1_token, 'a')
        
def test_invalid_used_handle():
   # person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
   # person2 = auth.auth_register('cs1532@cse.unsw.edu.au', 'abc1234', 'Marry', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_token = login_person1['token']
    with pytest.raises(InputError) as e:
        assert user.user_profile_sethandle(person1_token, 'marryjacobs')
        

#---------------------------------test the user_profile function--------------------------------------------#
def test_user_profile():
  #  person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_u_id = login_person1['u_id']
    person1_token = login_person1['token']
    assert user.user_profile(person1_token, person1_u_id) ==  {
        	'u_id': person1_u_id,
        	'email': 'cs1531@cse.unsw.edu.au',
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle': 'haydenjacobs',
        }, "user_profile fail"
    


#---------------------------------test the user_profile_setname function--------------------------------------------#
def test_user_profile_setname():
   # person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_u_id = login_person1['u_id']
    person1_token = login_person1['token']
    assert user.user_profile_setname(person1_token, name_first, name_last) == {}, "user_profile_setname fail"



#---------------------------------test the user_profile_setmail function--------------------------------------------#
def test_user_profile_setemail():
   # person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_u_id = login_person1['u_id']
    person1_token = login_person1['token']
    assert user.user_profile_setemail(person1_token, email) =={}#, "user_profile_setemail fail"




#---------------------------------test the user_profile_sethandle function--------------------------------------------#
def test_user_profile_sethandle():
   # person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    person1_u_id = login_person1['u_id']
    person1_token = login_person1['token']
    assert user.user_profile_sethandle(person1_token, handle_str) =={} #, "user_profile_sethandle fail"

