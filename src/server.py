'''
This file contains information about anything relating to the server.  The
methods in this file link all the routes to functions.
'''
import sys
from json import dumps
import os
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from error import InputError
from channel import *
from channels import *
from database import *
from other import *
import auth
from message_pin_react_functions import message_pin, message_unpin, message_react, message_unreact
from standup_functions import *
import message

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

root_dir = os.path.dirname(os.getcwd())

APP = Flask(__name__, static_folder=os.path.join(root_dir, 'static'))
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.config['STATIC_ROUTE'] = '/COMP1531/project/iteration3/back-end/T18A-WELV/src/static'
APP.register_error_handler(Exception, defaultHandler)
#------------------- msgserver--------------------------------------------------#
@APP.route("/message/send", methods=['POST'])
def message_send():
    jason = request.get_json()
    return message.message_send(jason['token'], jason['channel_id'], jason['message'])

@APP.route("/message/remove", methods=['DELETE'])
def message_remove():
    jason = request.get_json()
    message.message_remove(jason['token'], jason['message_id'])
    return {}

@APP.route("/message/edit", methods=['PUT'])
def message_edit():
    jason = request.get_json()
    message.message_edit(jason['token'], jason['message_id'], jason['message'])
    return {}

@APP.route("/message/sendlater", methods=['POST'])
def message_sendlater():
    jason = request.get_json()
    return message.message_sendlater(jason['token'], jason['channel_id'], jason['message'], jason['time_sent'])

#----------------------------------------------------------------------------#

#-------------------Auth Flask Server Methods---------------------#

@APP.route('/auth/login', methods=['POST'])
def login():
    '''
    Method will allow users to login using their credentials
    '''
    data = request.get_json()

    email = data['email']
    password = data['password']

    auth_data = auth.auth_login(email, password)

    u_id = auth_data['u_id']
    token = auth_data['token']

    return dumps({
        'u_id': u_id,
        'token': token,
    })

@APP.route('/auth/logout', methods=['POST'])
def logout():
    '''
    Method will allow users to logout using the token
    that they received with registering or loging in
    '''

    data = request.get_json()
    token = data['token']

    auth_data = auth.auth_logout(token)
    logout_status = auth_data['is_success']

    return dumps({
        'is_success': logout_status,
        })


@APP.route('/auth/register', methods=['POST'])
def register():
    '''
    Method will allow users to register using their name,
    email, and password
    '''

    data = request.get_json()

    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']

    auth_data = auth.auth_register(email, password, name_first, name_last)

    u_id = auth_data['u_id']
    token = auth_data['token']

    return dumps({
        'u_id': u_id,
        'token': token,
        })

@APP.route("/auth/passwordreset/request", methods=['POST'])
def return_password_request():
    '''
    Method will allow users to request to reset their password
    '''
    payload = request.get_json()
    email = payload['email']
    return auth.password_request(email)

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def return_password_reset():
    '''
    Method will allow users to reset their password
    '''
    payload = request.get_json()
    reset_code = payload['reset_code']
    new_password = payload['new_password']
    return auth.password_reset(reset_code, new_password)
#-----------------------------------------------------------------------------#

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

# Channels Functions

@APP.route("/channel/invite", methods=['POST'])
def return_channel_invite():
    '''
    Method will allow users to invite other members to join channel
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    return channel_invite(token, channel_id, u_id)

@APP.route("/channel/details", methods=['GET'])
def return_channel_details():
    '''
    Method will allow users to get channel details
    '''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return channel_details(token, channel_id)

@APP.route("/channel/messages", methods=['GET'])
def return_channel_messages():
    '''
    Method will allow users to get channel messages
    '''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    return channel_messages(token, channel_id, start)

@APP.route("/channel/leave", methods=['POST'])
def return_channel_leave():
    '''
    Method will allow users to leave channel
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    return channel_leave(token, channel_id)

@APP.route("/channel/join", methods=['POST'])
def return_channel_join():
    '''
    Method will allow users to join a channel
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    return channel_join(token, channel_id)

@APP.route("/channel/addowner", methods=['POST'])
def return_channel_addowner():
    '''
    Method will allow users to add owner to channel
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    return channel_addowner(token, channel_id, u_id)

@APP.route("/channel/removeowner", methods=['POST'])
def return_channel_removeowner():
    '''
    Method will allow users to remove owner from channel
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    return channel_removeowner(token, channel_id, u_id)

@APP.route("/channels/list", methods=['GET'])
def return_channels_list():
    '''
    Method will allow users to get list of their channels
    '''
    token = request.args.get('token')
    return channels_list(token)

@APP.route("/channels/listall", methods=['GET'])
def return_channels_listall():
    '''
    Method will allow users to get a list of all channels
    '''
    token = request.args.get('token')
    return channels_listall(token)

@APP.route("/channels/create", methods=['POST'])
def return_channel_create():
    '''
    Method will allow users to create new channel
    '''
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']
    return channels_create(token, name, is_public)

#--------------------message_pin/react methods-------------------------------------#
@APP.route("/message/react", methods=['POST'])
def react_mesage():
    '''
    Method will allow users to react to message
    '''
    payload = request.get_json()
    token = payload['token']
    react_id = payload['react_id']
    message_id = payload['message_id']
    return message_react(token, message_id, react_id)

@APP.route("/message/unreact", methods=['POST'])
def unreact_message():
    '''
    Method will allow users to unreact to message
    '''
    payload = request.get_json()
    token = payload['token']
    react_id = payload['react_id']
    message_id = payload['message_id']

    return message_unreact(token, message_id, react_id)

@APP.route("/message/pin", methods=['POST'])
def pin_message():
    '''
    Method will allow users to pin a message
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']

    return message_pin(token, message_id)


@APP.route("/message/unpin", methods=['POST'])
def unpin_message():
    '''
    Method will allow users to unpin a message
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']

    return message_unpin(token, message_id)



#------------------standup methods----------------------------------#
@APP.route('/standup/start', methods=['POST'])
def start_standup():
    '''
    Method will allow users to start a standup
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    length = int(payload['length'])
    return standup_start(token, channel_id, length)


@APP.route('/standup/active', methods=['GET'])
def is_active_standup():
    '''
    Method will allow users to check if a standup is active
    '''
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return standup_active(token, channel_id)

@APP.route('/standup/send', methods=['POST'])
def send_standup():
    '''
    Method will allow users to send a standup
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message_to_send = payload['message']
    return standup_send(token, channel_id, message_to_send)

@APP.route("/user/profile", methods=['GET'])
def return_profile():
    '''
    Method will allow users to get their profile details
    '''
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    return {'user':user_profile(token, u_id)}

@APP.route("/user/profile/setname", methods=['PUT'])
def return_set_name():
    '''
    Method will allow users to change their name
    '''
    payload = request.get_json()
    token = payload['token']
    name_first = payload['name_first']
    name_last = payload['name_last']
    return user_profile_setname(token, name_first, name_last)

@APP.route("/user/profile/setemail", methods=['PUT'])
def return_set_email():
    '''
    Method will allow users to change their email
    '''
    payload = request.get_json()
    token = payload['token']
    email = payload['email']
    return user_profile_setemail(token, email)

@APP.route("/user/profile/sethandle", methods=['PUT'])
def return_set_handle():
    '''
    Method will allow users to change their handle
    '''
    payload = request.get_json()
    token = payload['token']
    handle = payload['handle_str']
    return user_profile_sethandle(token, handle)

@APP.route('/user/profile/uploadphoto', methods=['POST'])
def upload_profile_photo():
    '''
    Method will allow users to change their profile image
    '''
    payload = request.get_json()
    token = payload['token']
    img_url = payload['img_url']
    x_start = payload['x_start']
    y_start = payload['y_start']
    x_end = payload['x_end']
    y_end = payload['y_end']
    return profile_picture(token, img_url, x_start, y_start, x_end, y_end)

@APP.route("/static/<filename>")
def download_photo(filename):
    '''
    Method will allow users to get their profile image
    '''
    #return os.path.join(APP.root_path, 'static')
    return send_from_directory(os.path.join(APP.root_path, 'static'), filename)

@APP.route("/users/all", methods=['GET'])
def return_all_users():
    '''
    Method will allow users to list all users on slackr
    '''
    token = request.args.get('token')
    return users_all(token)

@APP.route("/search", methods=['GET'])
def return_message_search():
    '''
    Method will allow users to search all messages
    '''
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return search(token, query_str)

@APP.route('/workspace/reset', methods=['POST'])
def reset_workspace():
    '''
    Method will allow users to reset the database
    '''
    return reset_db()

@APP.route('/admin/userpermission/change', methods=['POST'])
def change_user_permission():
    '''
    Method will allow users to change user permissions
    '''
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']
    return change_permission(token, u_id, permission_id)

@APP.route('/admin/user/remove', methods=['POST'])
def remove_the_user():
    '''
    Method will allow users to remove users
    '''
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    return remove_users(token, u_id)

@APP.route('/hangman/start', methods=['POST'])
def start_hangman():
    '''
    Method will allow users to start a game of hangman
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    return hangman_start(token, channel_id)

@APP.route('/hangman/guess', methods=['POST'])
def guess_hangman():
    '''
    Method will allow users to make a guess in hangman
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    character = payload['character']
    return hangman_guess(token, channel_id, character)

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8081))
