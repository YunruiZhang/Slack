from database import *
from channel import *
from error import *
import re

def user_profile(token, u_id):
    
    DATA = getData()
    
    foundFlag = False
    for users in DATA['users']:
        if int(users['u_id']) == int(u_id):
            foundFlag = True
            break

    if foundFlag == False:
        raise InputError('Invalid User ID')

    return_user = {
        'u_id' : users['u_id'],
        'email' : users['email'],
        'name_first' : users['name_first'],
        'name_last' : users['name_last'],
        'handle' : users['handle']
    }
    '''
    return_user['u_id'] = users['u_id']
    return_user['email'] = users['email']
    return_user['name_first'] = users['name_first']
    return_user['name_last'] = users['name_last']
    return_user['handle'] = users['handle']
    '''
    return return_user
    '''
    return {'user': {
        	'u_id': 1,
        	'email': 'cs1531@cse.unsw.edu.au',
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle': 'hjacobs',
        }
    }
    '''

def user_profile_setname(token, name_first, name_last):
    Data = getData()

    if not user_name_length_check(name_first):
        raise InputError('Length of first name is invalid') 
        
    if not user_name_length_check(name_last):
        raise InputError('Length of last name is invalid') 
   
    curr_u_id = verify_token(token)

    for user in Data['users']:
        if int(user['u_id']) == int(curr_u_id):
            user['name_first'] = name_first
            user['name_last'] = name_last
            break   
    
    return {
    }

def user_profile_setemail(token, email):
    Data = getData()
    
    if not user_email_check(email):
        raise InputError('Email has already been used')
    
    if not check(email):
        raise InputError("Email entered is not a valid email address")
        
    curr_u_id = verify_token(token)
   # if not curr_u_id:
    #    raise AccessError('Token Invalid')
    
    for user in Data['users']:
        if int(user['u_id']) == int(curr_u_id):
            break   
    
    user['email'] = email   
    
    return {
    }

def user_profile_sethandle(token, handle_str):
    DATA = getData()
    
    if not user_handle_length_check(handle_str):
        raise InputError('Length of handle is invalid')
        
    if not user_handle_check(handle_str):
        raise InputError('Handle has already been used')
    
    curr_u_id = verify_token(token)
   # if not curr_u_id:
   #     raise AccessError('Token Invalid')
       
    for user in DATA['users']:
        if int(user['u_id']) == int(curr_u_id):
            break   
    
    user['handle'] = handle_str
    
    
    return {
    }

def user_email_check(email):
    DATA = getData()
    for users in DATA['users']:
        if users['email'] == email:
            return False     
    return True

def user_handle_check(handle):
    DATA = getData()
    for users in DATA['users']:
        if users['handle'] == handle:
            return False     
    return True
    
def user_name_length_check(name):
    if len(name) == 0 or len(name) >50:
        return False    
    return True

def user_handle_length_check(handle):
    if len(handle) < 2 or len(handle) >20:
        return False    
    return True
    
# Make a regular expression 
# for validating an Email 
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
      
# Define a function for 
# for validating an Email 
def check(email):  
    if(re.search(regex,email)):  
        return True 
          
    else:  
        return False 

