from database import *
from channel import *
from error import *
import re


def users_all(token):
    all_user = []
    Data = getData()
    
    operate_u_id = verify_token(token)
    if not operate_u_id:
        raise AccessError('Token Invalid')
    for user in Data['users']:
        user.pop('password')
        user.pop('token')
        all_user.append(user)
    
    return all_user 
   


def search(token, query_str):
    search_message = []
    Data = getData()
    
    for single_message in Data['messages']:
        if query_str in single_message['message']:
            i = 0
            if search_message == []:
                search_message[0] = single_message
            else:
                while(i < len(single_message)):
                    time_origin = search_message[i]['time_created']
                    if single_message['time_created'] > time_origin:
                        search_message[1] = search_message[0]
                        search_message[0] = single_message
                        break
                    else:
                        i = i + 1
    
    return { 'messages' : search_message }
    
 