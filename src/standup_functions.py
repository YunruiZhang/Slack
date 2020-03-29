from database import getData, verify_token
import threading
import datetime
from message import get_msg_id
import database

'''
DATABASE = {
    'users' : [],
    'channels' : [],
    'messages' : []
}

'users' = [
    {   'u_id': u_id,
        'token': token,
        'name_first': name_first, 
        'name_last': name_last, 
        'password': password, 
        'email': email,
        }, 
]

"channels" : [
        {
            "channel_id":1,
            "public":1,
            "details" : {
                "name": "example name",
                "owner_members": [
                    {
                        "u_id": 1,
                        "name_first": "example first",
                        "name_last": "example last",
                    }
                ],
                "all_members": [
                    {
                        "u_id": 1,
                        "name_first": "example first",
                        "name_last": "example last",
                    }
                ],
            },
            "messages":[
                new_message, 
            ], 
            "standup": {
                "time_finish": None, 
                "message_buffer": [], 
                "is_active": False,
            }
        }, 
]

'messages' = {
    'message_id': message_id,
    'channel_id': channel_id,
}

new_message = {
        'message_id': message_id,
        'u_id': user_id,
        'message': message,
        'time': time,
        'reacts': [
            {
                'react_id': 1, 
                'u_ids': [], 
            }
        ],
        'is_pinned': False, 
}
'''


# POST
def standup_start(token, channel_id, length):
    '''For a given channel, start the standup period whereby 
    for the next "length" seconds if someone calls "standup_send" with a message, 
    it is buffered during the X second window then at the end of the X second window 
    a message will be added to the message queue in the channel 
    from the user who started the standup. 
    X is an integer that denotes the number of seconds that the standup occurs for'''
    D = database.getData()
    userID = verify_token(token)
    ch = get_channel_from_channelID(channel_id)

    # InputError:
    # Channel ID is not a valid channel
    if not check_channelID_valid(channel_id):
        raise InputError('Invalid channel ID')
    # An active standup is currently running in this channel
    if ch['standup']['is_active'] == True:
        raise InputError("Existing active standup in the channel")

    # start a standup
    # set up a timer
    t = threading.Timer(length, standup_end, args=[userID, ch])
    t.start()
    current_time = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    time_finish = current_time + length
    # update time_finish
    ch['standup']['time_finish'] = time_finish
    ch['standup']['is_active'] = True
    
    return {'time_finish': time_finish}


# GET
def standup_active(token, channel_id):
    '''For a given channel, return whether a standup is active in it, 
    and what time the standup finishes. 
    If no standup is active, then time_finish returns None'''
    # InputError:
    # Channel ID is not a valid channel
    if not check_channelID_valid(channel_id):
        raise InputError("Invalid channel ID")

    # check
    ch = get_channel_from_channelID(channel_id)
    time_finish = ch['stand']
    return { 'is_active': time_finish!=None, 'time_finish': time_finish }


# POST
def standup_send(token, channel_id, message):
    '''Sending a message to get buffered in the standup queue, 
    assuming a standup is currently active'''
    D = database.getData()
    ch = get_channel_from_channelID(channel_id)
    userID = verify_token(token)
    # InputError:
    # Channel ID is not a valid channel
    if not check_channelID_valid(channel_id):
        raise InputError("Invalid channel ID")
    # Message is more than 1000 characters
    if len(message) > 1000:
        raise InputError("Message too long")
    # An active standup is not currently running in this channel
    if ch['standup']['is_active'] == False:
        raise InputError('No current active standup')
    # AccessError:
    # The authorised user is not a member of the channel that the message is within
    if not check_user_in_channel(userID, ch):
        raise AccessError("User is not a member of the channel")
    
    # add standup message
    user = get_user_from_userID(userID)
    message_to_add = user['handle_str'] + ":" + message
    ch['standup']['message_buffer'].append(message_to_add)
    return {}


#######################################
# HELPER fs

def check_channelID_valid(channel_id):
    D = database.getData()
    for ch in D['channels']:
        if ch['channel_id'] == channel_id:
            return True
    return False

def get_channel_from_channelID(channel_id):
    D = database.getData()
    for ch in D['channels']:
        if ch['channel_id'] == channel_id:
            return ch
    return InputError("Invalid channel ID")

def standup_end(u_id, channel):
    D = database.getData()
    channel['standup']['time_finish'] = None
    message_summary = "|".join(channel['standup']['message_buffer'])
    # reset message_buffer after the standup
    channel['standup']['message_buffer'] = None
    # send the merged message in the end of the standup
    message_id = get_msg_id()
    database.new_message(message_id, channel['channel_id'], u_id, message_summary)



def get_user_from_userID(u_id):
    D = database.getData()
    for u in D['users']:
        if u[u_id] == u_id:
            return u
    raise InputError("Invalid user ID")



