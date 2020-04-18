'''
This file contains information about anything relating to channels.  The 
methods in this file relate to listing a single or all channels and creating
new channels. 
'''
from user import *
from flask import url_for
from database import *
from other import *
from error import InputError, AccessError

def channels_list(token):
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    channel_list = DATA['channels']
    list_to_return = []

    for channels in channel_list:
        for members in channels['details']['all_members']:
            if int(members['u_id']) == int(curr_u_id):
                list_to_return.append({
                    'channel_id':channels['channel_id'],
                    'name':channels['details']['name']
                })
            continue

    return {
        'channels': list_to_return
    }

def channels_listall(token):
    DATA = getData()

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    channel_list = DATA['channels']
    list_to_return = []

    for channels in channel_list:
        list_to_return.append({
            'channel_id':channels['channel_id'],
            'name':channels['details']['name']
        })

    return {
        'channels': list_to_return
    }

def channels_create(token, name, is_public):

    DATA = getData()

    if len(name) > 20:
        raise InputError("Name too long")

    curr_u_id = verify_token(token)
    if not curr_u_id:
        raise AccessError('Token Invalid')

    u_id_details = user_profile(token, curr_u_id)

    if DATA['channels']:
        channel_id = DATA['channels'][-1]['channel_id']+1
    else:
        channel_id = 1

    new_channel = {
        "channel_id":channel_id,
        "public": is_public,
        "details" : {
            "name": name,
            "owner_members": [
                {
                    "u_id": curr_u_id,
                    "name_first": u_id_details['name_first'],
                    "name_last": u_id_details['name_last'],
                    "profile_img_url": u_id_details['profile_img_url']
                }
            ],
            "all_members": [
                {
                    "u_id": curr_u_id,
                    "name_first": u_id_details['name_first'],
                    "name_last": u_id_details['name_last'],
                    "profile_img_url": u_id_details['profile_img_url']
                }
            ],
        },
        "messages": [],
        "standup": {
            "time_finish": None,
            "message_buffer": [],
            "is_active": False
        },
        "hangman": {
            "is_active":False,
            "word_to_guess": None,
            "guess_string": [],
            "guess_list" : []
        }
    }

    DATA['channels'].append(new_channel)
    update_database(DATA)
    return {
        'channel_id': channel_id
    }
