import datetime
import threading
from pytz import timezone
from database import *
from message import get_msg_id, message_send
from error import InputError, AccessError
from message_pin_react_functions import check_user_in_channel

# POST
def standup_start(token, channel_id, length):
    '''For a given channel, start the standup period whereby
    for the next "length" seconds if someone calls "standup_send" with a message,
    it is buffered during the X second window then at the end of the X second window
    a message will be added to the message queue in the channel
    from the user who started the standup.
    X is an integer that denotes the number of seconds that the standup occurs for'''
    DATA = getData()
    userID = verify_token(token)
    ch = get_channel_from_channelID(channel_id)
    ch1 = ch['standup']
    # InputError:
    # Channel ID is not a valid channel
    if not check_channelID_valid(channel_id):
        raise InputError('Invalid channel ID')
    # An active standup is currently running in this channel
    if ch1['is_active']:
        raise InputError("Existing active standup in the channel")

    # start a standup
    # set up a timer
    t = threading.Timer(length, standup_end, args=[userID, ch, token])
    t.start()
    current_time = datetime.datetime.utcnow().replace(tzinfo=timezone('UTC')).timestamp()
    time_finish = current_time + length
    # update time_finish
    ch['standup']['time_finish'] = time_finish
    ch['standup']['is_active'] = True

    update_database(DATA)
    return {'time_finish': time_finish}

# GET
def standup_active(token, channel_id):
    '''For a given channel, return whether a standup is active in it,
    and what time the standup finishes.
    If no standup is active, then time_finish returns None'''
    # InputError:
    # Channel ID is not a valid channel
    DATA = getData()
    if not verify_token(token):
        raise AccessError("Not an Authorised User")
    if not check_channelID_valid(channel_id):
        raise InputError("Invalid channel ID")

    # check
    ch = get_channel_from_channelID(channel_id)
    time_finish = ch['standup']['time_finish']
    is_active = ch['standup']['is_active']
    update_database(DATA)
    return {'is_active': is_active, 'time_finish': time_finish}

# POST
def standup_send(token, channel_id, message):
    '''Sending a message to get buffered in the standup queue,
    assuming a standup is currently active'''
    DATA = getData()
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
    if not ch['standup']['is_active']:
        raise InputError('No current active standup')
    # AccessError:
    # The authorised user is not a member of the channel that the message is within
    if not check_user_in_channel(userID, ch):
        raise AccessError("User is not a member of the channel")

    # add standup message
    user = get_user_from_userID(userID)
    message_to_add = user['handle_str'] + ": " + message
    ch['standup']['message_buffer'].append(message_to_add)
    update_database(DATA)
    return {}

#######################################
# HELPER fs

def check_channelID_valid(channel_id):
    D = getData()
    for ch in D['channels']:
        if ch['channel_id'] == channel_id:
            return True
    return False

def get_channel_from_channelID(channel_id):
    D = getData()
    for ch in D['channels']:
        if ch['channel_id'] == channel_id:
            return ch
    return InputError("Invalid channel ID")

def standup_end(u_id, channel,token):
    DATA= getData()
    channel['standup']['time_finish'] = None
    channel['standup']['is_active'] = False
    message_summary = "\n".join(channel['standup']['message_buffer'])
    # reset message_buffer after the standup
    channel['standup']['message_buffer'] = None
    # send the merged message in the end of the standup
    message_id = get_msg_id()
    #database.new_message(message_id, channel['channel_id'], u_id, message_summary)
    update_database(DATA)
    message_send(token,channel['channel_id'],message_summary)


def get_user_from_userID(u_id):
    D = getData()
    for u in D['users']:
        if u['u_id'] == u_id:
            return u
    raise InputError("Invalid user ID")
