'''
This file contains information about anything relating to a single channel.  The 
methods in this file relate to inviting/joining/leaving channels, adding/removing
owners, getting message details and channel details.  There are some helper
methods that just check the existence of channels and users.
'''
from user import *
from other import *
from channels import *
from database import *
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):
    '''
    Allows user's to invite other user's to their individual
    channel

    Parameters:
        token (str): Generated token from user's login session
        channel_id (str): Id relating to the individual channel
        u_id (str): User's id

    Returns:
        (dict): Empty dictionary
    '''
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    if not channel_id_check(DATA, channel_id) or not u_id_check(u_id):
        raise InputError('Invalid User or Channel ID')

    curr_channel = None
    for channels in DATA['channels']:
        if int(channels['channel_id']) == int(channel_id):
            curr_channel = channels
            break

    if not user_member_check(curr_channel, curr_u_id):
        raise AccessError('User is not a member of the channel')

    u_id_details = user_profile(token, u_id)

    user_to_add = {
        'u_id':u_id,
        'name_first': u_id_details['name_first'],
        'name_last': u_id_details['name_last']
    }

    curr_channel['details']['all_members'].append(user_to_add)
    update_database(DATA)
    return {}

def channel_details(token, channel_id):
    '''
    Gives a detailed dictionary that contains the information regarding
    the owner of the channel, and the users that have access to it

    Parameters:
        token (str): Generated token from user's login session
        channel_id (str): Id relating to the individual channel

    Returns:
        curr_channel['details'] (dictionary): Returns the all users in the channel
    '''
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    if not channel_id_check(DATA, channel_id):
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
    '''
    Gives a detailed dictionary that contains the information regarding
    all of the messages of a specific chanel

    Parameters:
        token (str): Generated token from user's login session
        channel_id (str): Id relating to the individual channel
        start (int): Beginning of the messages

    Returns:
        dict {
            messages (list): a list of dictionaries containg messages
            start (int): start of messages
            end (int): end of messages
        }
    '''
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    if not channel_id_check(DATA, channel_id):
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
    '''
    Allows a user to leave a given channel

    Parameters:
        token (str): Generated token from user's login session
        channel_id (str): Id relating to the individual channel

    Returns:
        (dict): Empty dictionary
    '''
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    if not channel_id_check(DATA, channel_id):
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

    update_database(DATA)

    return {
    }

def channel_join(token, channel_id):
    ''''
    Allows a user to join a given channel

    Parameters:
        token (str): Generated token from user's login session
        channel_id (str): Id relating to the individual channel

    Returns:
        (dict): Empty dictionary
    '''
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    if not channel_id_check(DATA, channel_id):
        raise InputError('Channel ID is invalid')

    curr_channel = None
    for channels in DATA['channels']:
        if int(channels['channel_id']) == int(channel_id):
            curr_channel = channels
            break

    if not user_owner_check(curr_channel, curr_u_id) and not curr_channel['public']:
        raise AccessError('User not an owner of private channel')

    u_id_details = user_profile(token, curr_u_id)

    user_to_add = {
        'u_id':curr_u_id,
        'name_first': u_id_details['name_first'],
        'name_last': u_id_details['name_last']
    }

    curr_channel['details']['all_members'].append(user_to_add)
    update_database(DATA)
    return {
    }

def channel_addowner(token, channel_id, u_id):
    '''
    Allows an owner to be added to a channel

    Parameters:
        token (str): Generated token from user's login session
        channel_id (str): Id relating to the individual channel
        u_id (str): User's id

    Returns:
        (dict): Empty dictionary
    '''
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    if not channel_id_check(DATA, channel_id):
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

    if not user_owner_check(curr_channel, curr_u_id) and not slackr_owner_check(curr_u_id):
        raise AccessError('AccessError')

    u_id_details = user_profile(token, u_id)

    user_to_add = {
        'u_id':u_id,
        'name_first': u_id_details['name_first'],
        'name_last': u_id_details['name_last']
    }

    curr_channel['details']['owner_members'].append(user_to_add)
    update_database(DATA)
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    '''
    Allows an owner to be removed from a channel

    Parameters:
        token (str): Generated token from user's login session
        channel_id (str): Id relating to the individual channel
        u_id (str): User's id

    Returns:
        (dict): Empty dictionary
    '''
    DATA = getData()

    if not channel_id_check(DATA, channel_id):
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

    if not user_owner_check(curr_channel, curr_u_id) and not slackr_owner_check(curr_u_id):
        raise AccessError('AccessError')

    for owners in curr_channel['details']['owner_members']:
        if owners['u_id'] == u_id:
            curr_channel['details']['owner_members'].remove(owners)
    update_database(DATA)
    return {
    }

def u_id_check(u_id):
    '''
    Checks if the user id is valid and being used already

    Parameters:
        u_id (str): User's id

    Returns:
        (bool): If the user_id is in the data or not
    '''
    DATA = getData()
    for users in DATA['users']:
        if int(users['u_id']) == int(u_id):
            return True
    return False


def channel_id_check(DATA, channel_id):
    '''
    Checks if the channel id is valid and being used already

    Parameters:
        channel_id (str): Id relating to the individual channel

    Returns:
        (bool): If the channel_id is in the data or not
    '''
    #DATA = getData()
    print(DATA)
    for channels in DATA['channels']:
        if int(channels['channel_id']) == int(channel_id):
            return True
    return False

def user_member_check(channel, u_id):
    '''
    Checks if the user is an authorized member of the channel

    Parameters:
        u_id (str): User's id
        channel_id (str): Id relating to the individual channel

    Returns:
        (bool): If the user is a member of not
    '''
    for members in channel['details']['all_members']:
        if int(members['u_id']) == int(u_id):
            return True
    return False

def user_owner_check(channel, u_id):
    '''
    Checks if the u_id is the owner of the channel

    Parameters:
        u_id (str): User's id
        channel_id (str): Id relating to the individual channel

    Returns:
        (bool): If the u_id is the owner or not
    '''
    for members in channel['details']['owner_members']:
        if int(members['u_id']) == int(u_id):
            return True
    return False

def slackr_owner_check(u_id):
    '''
    Checks if the u_id is the owner of slackr

    Parameters:
        u_id (str): User's id

    Returns:
        (bool): If the u_id is the owner or not
    '''
    user_list = getData()['users']
    for users in user_list:
        if users['u_id'] == u_id:
            if int(users['permission_id']) == 1:
                return True
    return False
