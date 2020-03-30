from database import *
from channel import *
from error import *

def users_all(token):
    all_user = []
    Data = getData()

    operate_u_id = verify_token(token)
    if not operate_u_id:
        raise AccessError('Token Invalid')
    for user in Data['users']:
        to_add = {
            'u_id': user['u_id'],
            'name_first': user['name_first'],
            'name_last':user['name_last'],
            'permission_id': user['permission_id'],
            'email': user['email'],
            'handle': user['handle']
        }
        all_user.append(to_add)

    return {"users":all_user}

def search(token, query_str):

    if not verify_token(token):
        raise AccessError('Invalid Token')

    search_message = []
    Data = getData()

    for channels in Data['channels']:
        curr_list = channels['messages']
        for i in curr_list:
            if query_str in i['message']:
                search_message.append(i)

    newlist = sorted(search_message, key=lambda k: k['time'])

    return {'messages' : newlist}
