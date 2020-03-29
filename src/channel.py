from other import *
from user import *
from channels import *
from database import *
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')


    if not channel_id_check(channel_id, token) or not u_id_check(u_id, token):
        raise InputError('Invalid User or Channel ID')

    curr_channel = None
    for channels in DATA['channels']:
        if int(channels['channel_id']) == int(channel_id):
            curr_channel = channels
            break

    if not user_member_check(curr_channel, curr_u_id):
        raise AccessError('User is not a member of the channel')

    u_id_details = user_profile(token,u_id)

    user_to_add = {
        'u_id':u_id,
        'name_first': u_id_details['name_first'],
        'name_last': u_id_details['name_last']
    }

    curr_channel['details']['all_members'].append(user_to_add)

    return {}

def channel_details(token, channel_id):
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    if not channel_id_check(channel_id, token):
        raise InputError('Channel ID is invalid')
    
    curr_channel = None
    for channels in DATA['channels']:
        if int(channels['channel_id']) == int(channel_id):
            curr_channel = channels
            break

    if not user_member_check(curr_channel, curr_u_id):
        raise AccessError('AccessError')

    return curr_channel['details']
    

def channel_messages(token, channel_id, start):
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    if not channel_id_check(channel_id, token):
        raise InputError('Channel id id invalid')

    curr_channel = None

    for channels in DATA['channels']:
        if int(channels['channel_id']) == int(channel_id):
            curr_channel = channels
            break

    if not user_member_check(curr_channel, curr_u_id):
        raise AccessError('User is not a member of this Channel')

    num_messages = len(curr_channel['messages'])

    start = int(start)

    if start > num_messages:
        raise InputError('Start index out of bounds')

    list_of_messages = []

    end = -1
    if start+50 <= num_messages:
        end = start+50

    # ASSUMING THAT THE LIST OF MESSAGES IS A LIST OF DICTIONARIES          

    return {
        'messages': curr_channel['messages'],
        'start': start,
        'end': end
    }

def channel_leave(token, channel_id):
    DATA = getData() 

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    if not channel_id_check(channel_id, token):
        raise InputError('InputError')

    curr_channel = None
    for channels in DATA['channels']:
        if int(channels['channel_id']) == int(channel_id):
            curr_channel = channels
            break

    if not user_member_check(curr_channel, curr_u_id):
        raise AccessError('AccessError')

    for members in curr_channel['details']['all_members']:
        if int(members['u_id']) == int(curr_u_id):
            curr_channel['details']['all_members'].remove(members) 

    return {
    }

def channel_join(token, channel_id):
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    if not channel_id_check(channel_id, token):
        raise InputError('Channel ID is invalid')

    curr_channel = None
    for channels in DATA['channels']:
        if int(channels['channel_id']) == int(channel_id):
            curr_channel = channels
            break

    if not user_owner_check(curr_channel,curr_u_id) and not curr_channel['public']:
        raise AccessError('User not an owner of private channel')

    u_id_details = user_profile(token,curr_u_id)

    user_to_add = {
        'u_id':curr_u_id,
        'name_first': u_id_details['name_first'],
        'name_last': u_id_details['name_last']     
    }


    curr_channel['details']['all_members'].append(user_to_add) 

    return {
    }

def channel_addowner(token, channel_id, u_id):
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    if not channel_id_check(channel_id, token):
        raise InputError('InputError')

    if not curr_u_id:
        raise AccessError('AccessError')

    curr_channel = None
    for channels in DATA['channels']:
        if channels['channel_id'] == channel_id:
            curr_channel = channels
            break

    if user_owner_check(curr_channel, u_id):
        raise InputError('InputError')

    if not user_owner_check(curr_channel, curr_u_id):
        raise AccessError('AccessError')

    u_id_details = user_profile(token,u_id)

    user_to_add = {
        'u_id':u_id,
        'name_first': u_id_details['name_first'],
        'name_last': u_id_details['name_last']
    }

    curr_channel['details']['owner_members'].append(user_to_add)

    return {
    }

    
def channel_removeowner(token, channel_id, u_id):
    DATA = getData()

    if not channel_id_check(channel_id, token):
        raise InputError('InputError')

    curr_u_id = verify_token(token)
    
    if not curr_u_id:
        raise AccessError('AccessError')

    curr_channel = None    

    for channels in DATA['channels']:
        if channels['channel_id'] == channel_id:
            curr_channel = channels
            break

    if not user_owner_check(curr_channel, u_id):
        raise InputError('InputError')

    if not user_owner_check(curr_channel, curr_u_id):
        raise AccessError('AccessError')
   
    for owners in curr_channel['details']['owner_members']:
        if owners['u_id'] == u_id:
            curr_channel['details']['owner_members'].remove(owners)

    return {
    }

def u_id_check(u_id, token):
    DATA = getData()
    for users in DATA['users']:
        if int(users['u_id']) == int(u_id):
            return True
            break
    return False


def channel_id_check(channel_id, token):
    DATA = getData()
    for channels in DATA['channels']:
        if int(channels['channel_id']) == int(channel_id):
            return True
            break
    return False

def user_member_check(channel, u_id):
    for members in channel['details']['all_members']:
        if int(members['u_id']) == int(u_id):
            return True
            break        
    return False

def user_owner_check(channel, u_id):
    for members in channel['details']['owner_members']:
        if int(members['u_id']) == int(u_id):
            return True
            break        
    return False
