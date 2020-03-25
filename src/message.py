import database
from error import AccessError, InputError



def message_send(token, channel_id, message):
    #check whether the length of msg is smaller than 1000
    if len(message) > 1000:
        raise InputError("Message is longer than 1000 characters")
    #verify the token
    var = database.verify_token(token)
    if var == False:
        raise AccessError("The token does not exist")
    # check if the channel exist and whether the user is in it
    flag = check_in_channel(var, channel_id)
    if flag == 2:
        raise InputError("channel doesn't exist")
    if flag == 1:
        raise AccessError("user is not in the channel")
    message_id = get_msg_id()
    database.new_message(message_id, channel_id, var, message)
    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):
    # check whether the token is valid
    user_id = database.verify_token(token)
    if user_id == False:
        raise AccessError("The token does not exist")
    #check whether the message exist
    channel = check_msg(message_id)
    if channel == False:
        raise InputError("The message does not exist")
    #check whether the user have access to remove it
    access = check_access(user_id, channel, message_id)
    if access == False:
        raise AccessError("The user don't have permission to remove this message")
    #remove it
    data = database.getData()
    for i in data['messages']:
        if i['message_id'] == message_id:
            data['messages'].remove(i)
            break
    return {
    }

def message_edit(token, message_id, message):
    return {
    }

def message_sendlater(token, channel_id, message, time_sent):
    return{
        'message_id': 1,
    }


def check_in_channel(user_id, channel_id):
    data = database.getData()
    found_channel = 0
    found_user = 0
    for i in database['channels']:
        if i['channel_id'] == channel_id:
            found_channel = 1
            for x in i['all_members']:
                if x['u_id'] == user_id:
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
    if len(database['messages']) == 0:
        return 0
    else: 
        return data['messages'][-1]['message_id'] + 1

def check_msg(message_id):
    data = database.getData()
    for i in data['messages']:
        if i['message_id'] == message_id:
            return i['channel_id']
    return False

def check_access(user_id, channel_id, message_id):
    data = database.getData
    sender = 0
    owner = 0
    #check whether user_id is the sender of the message
    for i in data['channels']:
        if i['channel_id'] == channel_id:
            for x in i['messages']:
                if x[message_id] == message_id:
                    if x[u_id] == user_id:
                        sender = 1
                        break
    

    for ch in data['channels']:
        if ch['channel_id'] == channel_id:
            for owner in ch['owner_members']:
                if owner['u_id'] == user_id:
                    owner = 1
                    break
    
    if sender == 1 or owner == 1:
        return True
    else:
        return False
