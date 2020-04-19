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
    """ Sends a message

    Parameters:
        token (str): The token of the active user
        channel_id(int): ID of the current channel
        message(str): Message to send

    Returns:
        message_id(int): ID of the message

    """
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
    """ Remove a message

    Parameters:
        token (str): The token of the active user
        message_id(int): The ID of the message to remove

    Returns:
        None

    """
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
    """ Edit a message

    Parameters:
        token (str): The token of the active user
        message_id(int): The ID of the message to edit
        message(str): The new message

    Returns:
        None

    """
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
    """ Send a meessage later

    Parameters:
        token (str): The token of the active user
        channel_id(int): The ID of the current channel
        message(str): The message to send
        time_sent(int (UNIX timestamp)): The time to send the message

    Returns:
        message_id(int):The ID of the message

    """
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
    """ Checks if user is in channel

    Parameters:
        user_id (int): The ID of the user
        channel_id (int): The channel ID

    Returns:
        0 stands for the channel id is valid and the user is in the channel
        1 stands for user is not in the channel
        2 stands for invalid channel id
    """
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
    """ Generate a message ID

    Parameters:
        None

    Returns:
        message_id(int): The ID for the new message
    """

    data = database.getData()
    if not data['messages']:
        return 1
    return data['messages'][-1]['message_id'] + 1

def check_msg(message_id):
    #print(message_id)
    """ Gets channel message is in if it exists

    Parameters:
        message (int): The message ID

    Returns:
        if True:
            channel_id(int):The ID of the channel the message is in
        if False:
            False
    """
    data = database.getData()
    for i in data['messages']:
        #print(i)
        if int(i['message_id']) == int(message_id):
            #print(i['channel_id'])
            return i['channel_id']
    return False

def check_access(user_id, channel_id, message_id):
    """ Checks if user is in sender or owner

    Parameters:
        user_id (int): The ID of the user
        channel_id (int): The channel ID
        message_id (int): The ID of the message

    Returns:
        bool : True or False if valid
    """
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
    """ Removes message from database

    Parameters:
        message_id (int): The ID of the message
        channel_id (int): The channel ID

    Returns:
       None
    """
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
    """ Edit message in database

    Parameters:
        message_id (int): The ID of the message
        channel_id (int): The channel ID
        message(str): The new message

    Returns:
       None
    """
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
    """ Sends a message later

    Parameters:
        message_id (int): The ID of the message
        channel_id (int): The channel ID
        user_id(int): The user ID
        message(str): Message to send
        time_sent(int (UNIX timestamp)): The time to send the message

    Returns:
       None
    """
    #wait until time_sent
    while datetime.now().replace(tzinfo=timezone.utc).timestamp() < int(time_sent):
        sleep(0.1)
    database.new_message(message_id, channel_id, user_id, message)
    return{
    }
