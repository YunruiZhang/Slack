import database
from error import AccessError, InputError
from datetime import datetime
import threading
from time import sleep

def message_send(token, channel_id, message):
    #check whether the length of msg is smaller than 1000
    if len(message) > 1000:
        raise InputError(description = 'Message is longer than 1000 characters')
    #verify the token
    var = database.verify_token(token)
    if var == False:
        raise AccessError(description = 'The token does not exist')
    # check if the channel exist and whether the user is in it
    flag = check_in_channel(var, channel_id)
    if flag == 2:
        raise InputError(description = 'channel does not exist')
    if flag == 1:
        raise AccessError(description = 'user is not in the channel')
    message_id = get_msg_id()
    database.new_message(message_id, channel_id, var, message)
    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):
    # check whether the token is valid
    user_id = database.verify_token(token)
    if user_id == False:
        raise AccessError(description = 'The token does not exist')
    #check whether the message exist
    channel = check_msg(message_id)
    if channel == False:
        raise InputError(description = 'The message does not exist')
    #check whether the user have access to remove it
    access = check_access(user_id, channel, message_id)
    if access == False:
        raise AccessError(description = 'The user doed not have permission to remove this message')
    #remove it
    remove(message_id, channel)
    
    return {
    }

def message_edit(token, message_id, message):
     # check whether the token is valid
    user_id = database.verify_token(token)
    if user_id == False:
        raise AccessError(description = 'The token does not exist')
    #check whether the message exist
    channel = check_msg(message_id)
    if channel == False:
        raise InputError(description = 'The message does not exist')
    #check whether the user have access to remove it
    access = check_access(user_id, channel, message_id)
    if access == False:
        raise AccessError(description = 'The user does not have permission to remove this message')
    if message == '':
        remove(message_id, channel)
    edit(message_id, channel, message)
    return {
    }

def message_sendlater(token, channel_id, message, time_sent):
    #if time_sent is in the past raise error
    if time_sent < str(datetime.now()):
        raise InputError(description = 'Cannot send a message in the past')
    #check whether the length of msg is smaller than 1000
    if len(message) > 1000:
        raise InputError(description = 'Message is longer than 1000 characters')
    #verify the token
    var = database.verify_token(token)
    if var == False:
        raise AccessError(description = 'The token does not exist')
    # check if the channel exist and whether the user is in it
    flag = check_in_channel(var, channel_id)
    if flag == 2:
        raise InputError(description = 'channel does not exist')
    if flag == 1:
        raise AccessError(description = 'user is not in the channel')
    message_id = get_msg_id()
    #send the msg in time_sent
    threading.Thread(target=later_send, args=(message_id, channel_id, var, message, time_sent)).start()
    return{
        'message_id': message_id,
    }


def check_in_channel(user_id, channel_id):
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
    else:
        return 2

def get_msg_id():
    data = database.getData()
    if len(data['messages']) == 0:
        return 1
    else: 
        return data['messages'][-1]['message_id'] + 1

def check_msg(message_id):
    #print(message_id)
    data = database.getData()
    for i in data['messages']:
        #print(i)
        if int(i['message_id']) == int(message_id):
            #print(i['channel_id'])
            return i['channel_id']
    return False

def check_access(user_id, channel_id, message_id):
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
    
    if sender == 1 or owner == 1:
        return True
    else:
        return False

def remove(message_id, channel_id):
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
    return{
    }

def edit(message_id, channel_id, message):
    #edit message it in channel
    data = database.getData()
    for j in data['channels']:
        if int(j['channel_id']) == int(channel_id):
            for x in j['messages']:
                if int(x['message_id']) == int(message_id):
                    x['message'] = message
                    break
    return{
    }
def later_send(message_id, channel_id, user_id, message, time_sent):
    #wait until time_sent
    while str(datetime.now()) < time_sent:
        sleep(0.1)
    database.new_message(message_id, channel_id, user_id, message)
    return{
    }

