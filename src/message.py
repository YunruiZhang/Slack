'''
This file contains information about anything relating to messages.  The 
methods in this file relate to sending, removing, editing and the send 
later function.  There are some helper methods that just check the 
existence of channels and users.
'''
from datetime import datetime, timezone
import threading
from time import sleep
from error import AccessError, InputError
import database

def message_send(token, channel_id, message):
    '''
    Creating a new message and sending it to a specific channel

    Parameters:
        token (str): Generated token from user's login session
        channel_id (str): Id relating to the individual channel
        message (str): Message that will be sent

    Returns:
        dict {
            message_id (str): Id of the new message
        }
    '''
    #check whether the length of msg is smaller than 1000
    if len(message) > 1000:
        raise InputError(description='Message is longer than 1000 characters')
    #verify the token
    var = database.verify_token(token)
    if not var:
        raise AccessError(description='The token does not exist')
    # check if the channel exist and whether the user is in it
    flag = check_in_channel(var, channel_id)
    if flag == 2:
        raise InputError(description='channel does not exist')
    if flag == 1:
        raise AccessError(description='user is not in the channel')
    message_id = get_msg_id()
    database.new_message(message_id, channel_id, var, message)

    return {
        'message_id': message_id
    }

def message_remove(token, message_id):
    '''
    Removes a message from a specific channel

    Parameters:
        token (str): Generated token from user's login session
        message (str): Message that will be removed

    Returns:
        (dict): empty dictionary
    '''
    # check whether the token is valid
    user_id = database.verify_token(token)
    if not user_id:
        raise AccessError(description='The token does not exist')
    #check whether the message exist
    channel = check_msg(message_id)
    if not channel:
        raise InputError(description='The message does not exist')
    #check whether the user have access to remove it
    access = check_access(user_id, channel, message_id)
    if not access:
        raise AccessError(description='The user doed not have permission to remove this message')
    #remove it
    remove(message_id, channel)

    return {
    }

def message_edit(token, message_id, message):
    '''
    Edits a message from a specific channel

    Parameters:
        token (str): Generated token from user's login session
        message_id (str): Message id of message that will be edited
        message (str): Message that will be edited

    Returns:
        (dict): empty dictionary
    '''
    if len(message) > 1000:
        raise InputError(description='Message is longer than 1000 characters')
     # check whether the token is valid
    user_id = database.verify_token(token)
    if not user_id:
        raise AccessError(description='The token does not exist')
    #check whether the message exist
    channel = check_msg(message_id)
    if not channel:
        raise InputError(description='The message does not exist')
    #check whether the user have access to remove it
    access = check_access(user_id, channel, message_id)
    if not access:
        raise AccessError(description='The user does not have permission to remove this message')
    if message == '':
        remove(message_id, channel)
    edit(message_id, channel, message)
    return {
    }

def message_sendlater(token, channel_id, message, time_sent):
    '''
    Sends a delayed message to a specific channel

    Parameters:
        token (str): Generated token from user's login session
        channel_id (str): Id relating to the individual channel
        message (str): Message that will be edited
        time_sent (int): Time until sending message

    Returns:
        dict {
            message_id (str): The id of the message that will be sent
        }
    '''
    #if time_sent is in the past raise error
    if time_sent < datetime.now().timestamp():
        raise InputError(description='Cannot send a message in the past')
    #check whether the length of msg is smaller than 1000
    if len(message) > 1000:
        raise InputError(description='Message is longer than 1000 characters')
    #verify the token
    var = database.verify_token(token)
    if not var:
        raise AccessError(description='The token does not exist')
    # check if the channel exist and whether the user is in it
    flag = check_in_channel(var, channel_id)
    if flag == 2:
        raise InputError(description='channel does not exist')
    if flag == 1:
        raise AccessError(description='user is not in the channel')
    message_id = get_msg_id()
    #send the msg in time_sent
    threading.Thread(target=later_send, args=(message_id, channel_id, var, message, time_sent)).start()
    return{
        'message_id': message_id,
    }


def check_in_channel(user_id, channel_id):
    '''
    Checks if a user is in a channel

    Parameters:
        user_id (str): User's id
        channel_id (str): Id relating to the individual channel

    Returns:
        (int): 0, 1 or 2 depending on if the user is in the channel and valid
    '''
    data = database.getData()
    found_channel = 0
    found_user = 0
    for i in data['channels']:
        if int(i['channel_id']) == int(channel_id):
            found_channel = 1
            #print(i)
            for x in i['details']['all_members']:
                if int(x['u_id']) == int(user_id):
                    found_user = 1
    # 0 stands for the channel id is valid and the user is in the channel
    # 1 stands for user is not in the channel
    # 2 stands for invalid channel id
    if found_user == 1 and found_channel == 1:
        return 0
    elif found_channel == 1 and found_user == 0:
        return 1
    return 2

def get_msg_id():
    '''
    Helper method that returns the message id

    Returns:
        (str): message_id
    '''
    data = database.getData()
    if not data['messages']:
        return 1
    return data['messages'][-1]['message_id'] + 1

def check_msg(message_id):
    '''
    Helper method that checks if the message exists

    Returns:
        (bool): if the message_id does not exist
        (str): if the message_id exists
    '''
    #print(message_id)
    data = database.getData()
    for i in data['messages']:
        #print(i)
        if int(i['message_id']) == int(message_id):
            #print(i['channel_id'])
            return i['channel_id']
    return False

def check_access(user_id, channel_id, message_id):
    '''
    Helper method that checks if user has permission to
    be in the channel

    Parameters:
        user_id (str): User's id
        channel_id (str): Id relating to the individual channel
        message_id (str): Id relating to a specific message in a channel

    Returns:
        (bool): if the user_id does not exist
    '''
    data = database.getData()
    sender = 0
    owner = 0
    #check whether user_id is the sender of the message
    for channel in data['channels']:
        if int(channel['channel_id']) == int(channel_id):
            for x in channel['messages']:
                if int(x['message_id']) == int(message_id):
                    if int(x['u_id']) == int(user_id):
                        sender = 1
                        break

    for ch in data['channels']:
        if int(ch['channel_id']) == int(channel_id):
            for owner in ch['details']['owner_members']:
                if int(owner['u_id']) == int(user_id):
                    owner = 1
                    break

    return sender == 1 or owner == 1

def remove(message_id, channel_id):
    '''
    Helper method that removes a message from a channel

    Parameters:
        channel_id (str): Id relating to the individual channel
        message_id (str): Id relating to a specific message in a channel

    Returns:
        (dict): emtpy dictionary
    '''
    #remove it in message list inside database
    data = database.getData()
    for i in data['messages']:
        if int(i['message_id']) == int(message_id):
            data['messages'].remove(i)
            break
    #remove it in channel
    for j in data['channels']:
        if int(j['channel_id']) == int(channel_id):
            for x in j['messages']:
                if int(x['message_id']) == int(message_id):
                    j['messages'].remove(x)
                    break
    database.update_database(data)
    return{
    }

def edit(message_id, channel_id, message):
    '''
    Helper method that edits a message from a channel

    Parameters:
        message_id (str): Id relating to a specific message in a channel
        channel_id (str): Id relating to the individual channel
        message (str): The new message (replacing the old one)

    Returns:
        (dict): emtpy dictionary
    '''
    #edit message it in channel
    data = database.getData()
    for j in data['channels']:
        if int(j['channel_id']) == int(channel_id):
            for x in j['messages']:
                if int(x['message_id']) == int(message_id):
                    x['message'] = message
                    break
    database.update_database(data)
    return{
    }

def later_send(message_id, channel_id, user_id, message, time_sent):
    '''
    Helper method that sends a delayed message

    Parameters:
        message_id (str): Id relating to a specific message in a channel
        channel_id (str): Id relating to the individual channel
        user_id (str): User's id
        message (str): The new message (replacing the old one)
        time_sent (int): Time delayed to send the message

    Returns:
        (dict): emtpy dictionary
    '''
    #wait until time_sent
    while datetime.now().replace(tzinfo=timezone.utc).timestamp() < int(time_sent):
        sleep(0.1)
    database.new_message(message_id, channel_id, user_id, message)
    return{
    }
