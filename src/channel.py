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
    """ Invites user with u_id to join channel with channel_id

    Parameters:
        u_id (int): User ID
        token (str): The token of the active user
        channel_id (int): Channel ID

    Returns:
        {}: Empty dictionary

    """
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
    """ Gets the details of channel with channel_id

    Parameters:
        channel_id (int): Channel ID
        token (str): The token of the active user

    Returns:
        name (string): Name of the channel
        owner_members (list): List of owner members
        all_members (list): List of all members

    """
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
    """ Gets the messages of channel with channel_id

    Parameters:
        channel_id (int): Channel ID
        token (str): The token of the active user
        start(int): Starting index for the messages

    Returns:
        messages(list): List of all messages
        start(int): Starting index
        end(int): Ending index

    """
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
    """ Active user leaves channel with channel_id

    Parameters:
        channel_id (int): Chennel ID
        token (str): The token of the active user

    Returns:
        {}: Empty dictionary

    """
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
    """ Lets active user join channel with channel_id

    Parameters:
        channel_id (int): Channel ID
        token (str): The token of the active user

    Returns:
        {}:Empty dictionary

    """
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
    """ Add user with u_id as owner to channel with channel_id

    Parameters:
        u_id (int): User ID
        channel_id(int): Channel ID
        token (str): The token of the active user

    Returns:
        {}: Empty Dictionary

    """
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
    """ Removes user with u_id as owner of channel with channel_id

    Parameters:
        u_id (int): User ID
        channel_id(int): Channel ID
        token (str): The token of the active user

    Returns:
        {}: Empty Dictionary

    """
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
    """ Checks to see if the u_id is valid

    Parameters:
        u_id(int): User ID

    Returns:
        bool: True or False whether it's valid

    """
    DATA = getData()
    for users in DATA['users']:
        if int(users['u_id']) == int(u_id):
            return True
    return False


def channel_id_check(DATA, channel_id):
    """ Checks to see if the channel_id is valid

    Parameters:
        channel_id(int): Channel ID
        DATA (dictionary): Current state of the database

    Returns:
        bool: True or False whether it's valid

    """
    #DATA = getData()
    #print(DATA)
    for channels in DATA['channels']:
        if int(channels['channel_id']) == int(channel_id):
            return True
    return False

def user_member_check(channel, u_id):
    """ Checks to see if the u_id is member

    Parameters:
        u_id(int): User ID
        channel(dictionary): Currrent channel

    Returns:
        bool: True or False whether it's true

    """
    for members in channel['details']['all_members']:
        if int(members['u_id']) == int(u_id):
            return True
    return False

def user_owner_check(channel, u_id):
    """ Checks to see if the u_id is owner

    Parameters:
        u_id(int): User ID
        channel(dictionary): Current channel

    Returns:
        bool: True or False whether it's true

    """
    for members in channel['details']['owner_members']:
        if int(members['u_id']) == int(u_id):
            return True
    return False

def slackr_owner_check(u_id):
    """ Checks to see if the u_id is slackr owner

    Parameters:
        u_id(int): User ID

    Returns:
        bool: True or False whether it's true

    """
    user_list = getData()['users']
    for users in user_list:
        if users['u_id'] == u_id:
            if int(users['permission_id']) == 1:
                return True
    return False
