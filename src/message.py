import database.py
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
    #get the database
    data = database.getData()

    return {
        'message_id': 1,
    }

def message_remove(token, message_id):
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
    if found_user == 1 and found channel == 1:
        return 0
    elif found_channel == 1 and found_user == 0:
        return 1
    else:
        return 2