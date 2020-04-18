'''
This file contains information about anything relating to message pins
and reacts.  The methods in this file relate to reacting and pinning 
messages.  There are some helper methods that just check the existence 
of channels and users.
'''
from database import *
from error import AccessError, InputError
#from standup_functions import get_channel_from_channelID

# POST
def message_react(token, message_id, react_id):
    '''Given a message within a channel the authorised
    user is part of, add a "react" to that particular message'''
    DATA = getData()
    print(message_id)
    msg = get_message_from_messageID(DATA, message_id)
    ch = get_channel_from_msgID(DATA, message_id)
    userID = verify_token(token)
    # /InputError when any of:
    # Message_id is not a valid message within a channel that
    #the authorised user has joined -> user is not in the message's channel
    if not check_valid_msg(message_id):
        raise InputError('Invalid message ID')
    if not check_user_in_channel(userID, ch):
        raise InputError("User not in message's channel")
    # React_id is not a valid React ID. The only valid react ID the frontend has is 1
    if react_id != 1:
        raise InputError('Invalid react ID')
    # Message with ID message_id already contains an active React with ID react_id
    for r in msg['reacts']:
        if r['react_id'] == react_id:
            for users in r['u_ids']:
                if users == userID:
                    raise InputError("Same react already exsited")
            break

    # Non-exception: add react
    #new = {
    #    'react_id': react_id,
    #    'u_ids': userID,
    #    'is_this_user_reacted': True
    #}
    r['u_ids'].append(userID)
    update_database(DATA)
    #print(DATA)
    DATA = getData()
    #print(DATA)
    #msg['reacts']['is_this_user_reacted'] = True
    return {}


# POST
def message_unreact(token, message_id, react_id):
    '''Given a message within a channel the authorised user is part of,
    remove a "react" to that particular messageGiven a message within a
    channel the authorised user is part of, remove a "react" to that particular message'''
    DATA = getData()
    msg = get_message_from_messageID(DATA, message_id)
    ch = get_channel_from_msgID(DATA, message_id)
    userID = verify_token(token)
    # InputError:
    # Message_id is not a valid message within a channel that the authorised user has joined
    if not check_valid_msg(message_id):
        raise InputError('Invalid message ID')
    if not check_user_in_channel(userID, ch):
        raise InputError("User not in message's channel")
    # React_id is not a valid React ID
    if react_id != 1:
        raise InputError('Invalid react ID')
    # Message with ID message_id does not contain an active React with ID react_id
    reacted = False

    for r in msg['reacts']:
        if r['react_id'] == react_id:
            for users in r['u_ids']:
                if users == userID:
                    reacted = True
                    r['u_ids'].remove(users)

    if not reacted:
        raise InputError('No such react in given message')

    # Non-exception: remove react
    #for r in msg['reacts']:
    #    if r['react_id'] == react_id:
    #        msg['reacts'].remove(r)
    update_database(DATA)
    return {}

# POST
def message_pin(token, message_id):
    '''Given a message within a channel, mark it as "pinned" to be
    given special display treatment by the frontend'''
    DATA = getData()
    msg = get_message_from_messageID(DATA, message_id)
    userID = verify_token(token)
    ch = get_channel_from_msgID(DATA, message_id)
    # -InputError:
    # message_id is not a valid message
    if not check_valid_msg(message_id):
        raise InputError("Invalid message ID")
    # The authorised user is not an owner
    if not check_owner(ch, userID):
        raise InputError("User is not an owner")
    # Message with ID message_id is already pinned
    if msg['is_pinned']:
        raise InputError("Given message already pinned")
    # -AccessError:
    # The authorised user is not a member of the channel that the message is within
    if not check_user_in_channel(userID, ch):
        raise AccessError("User is not a member of the channel")

    # Non-exception: pin the message
    msg['is_pinned'] = True
    update_database(DATA)
    return {}

# POST
def message_unpin(token, message_id):
    '''Given a message within a channel, remove it's mark as unpinned'''
    DATA = getData()
    msg = get_message_from_messageID(DATA, message_id)
    userID = verify_token(token)
    ch = get_channel_from_msgID(DATA, message_id)
    # InputError:
    # message_id is not a valid message
    if not check_valid_msg(message_id):
        raise InputError("Invalid message ID")
    # The authorised user is not an owner
    if not check_owner(ch, userID):
        raise InputError("User is not an owner")
    # Message with ID message_id is already unpinned
    if not msg['is_pinned']:
        raise InputError("Given message is already UN-pinned")
    # AccessError:
    # The authorised user is not a member of the channel that the message is within
    if not check_user_in_channel(userID, ch):
        raise AccessError('User is not a member of the channel')

    # Non-exception: unpin the message
    msg['is_pinned'] = False
    update_database(DATA)
    return {}

#################
# HELPER funcitons

def get_channel_from_msgID(D, message_id):
    #D = getData()
    #raise InputError(f"{D}")
    for sm in D['messages']:
        if sm['message_id'] == int(message_id):
            for ch in D['channels']:
                if ch['channel_id'] == sm['channel_id']:
                    return ch
    return InputError("channel not found")


def get_message_from_messageID(D, message_id):
    ch = get_channel_from_msgID(D, message_id)
    for m in ch['messages']:
        if m['message_id'] == message_id:
            return m
    return InputError("message not found")


def check_valid_msg(message_id):
    D = getData()
    for sm in D['messages']:
        if sm['message_id'] == message_id:
            return True
    return False


def check_user_in_channel(u_id, ch):
    for user in ch['details']['all_members']:
        if u_id == user['u_id']:
            return True
    return False




def check_owner(ch, u_id):
    is_owner = False
    for u in ch['details']['owner_members']:
        if u['u_id'] == u_id:
            is_owner = True
    return is_owner
