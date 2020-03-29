import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from channel import *
from channels import *
from database import *
from other import *
import auth
from message_pin_react_functions import message_pin, message_unpin, message_react, message_unreact
from standup_functions import standup_start, standup_active, standup_send
#from message_pin_react_functions import message_pin, message_unpin, message_react, message_unreact
#from standup_functions import standup_start, standup_active, standup_send


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

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
#------------------- msgserver-----------------------------------------------------------#
@APP.route("/message/send", methods = ['POST'])
def message_send():
    jason = request.get_json()
    msg_id = message.message_send(jason['token'], jason['channel_id'], jason['message'])
    return dumps({
        'message_id': msg_id
    })
    
@APP.route("/message/remove", methods = ['DELETE'])
def message_remove():
    jason = request.get_json()
    message.message_remove(jason['token'], jason['message_id'])
    return {}

@APP.route("/message/edit", methods = ['PUT'])
def message_edit():
    jason = request.get_json()
    message.message_edit(jason['token'], jason['message_id'], jason['message'])
    return {}

@APP.route("/message/sendlater", methods = ['POST'])
def message_sendlater():
    jason= request.get_json()
    id = message.message_sendlater(jason['token'], jason['channel_id'], jason['message'], jason['time_sent'])
    return dumps({
        'message_id': id
    })
#----------------------------------------------------------------------------------------------------------------------#

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
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    return channel_invite(token,channel_id,u_id)

@APP.route("/channel/details", methods=['GET'])
def return_channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return channel_details(token,channel_id)

@APP.route("/channel/messages", methods=['GET'])
def return_channel_messages():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    return channel_messages(token,channel_id,start)

@APP.route("/channel/leave", methods=['POST'])
def return_channel_leave():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    return channel_leave(token, channel_id)

@APP.route("/channel/join", methods=['POST'])
def return_channel_join():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    return channel_join(token,channel_id)

@APP.route("/channel/addowner", methods=['POST'])
def return_channel_addowner():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    return channel_addowner(token,channel_id,u_id)

@APP.route("/channel/removeowner", methods=['POST'])
def return_channel_removeowner():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']  
    return channel_removeowner(token,channel_id,u_id)

@APP.route("/channels/list", methods=['GET'])
def return_channels_list():
    token = request.args.get('token') 
    return channels_list(token)

@APP.route("/channels/listall", methods=['GET'])
def return_channels_listall():
    token = request.args.get('token') 
    return channels_listall(token)

@APP.route("/channels/create", methods=['POST'])
def return_channel_create():
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']    
    return channels_create(token,name,is_public) 


#--------------------message_pin/react methods-------------------------------------#
@APP.route("/message/react", methods=['POST'])
def react_mesage():
    payload = request.get_json()
    token = payload['token']
    react_id = int(payload['react_id'])
    message_id = int(payload['message_id'])
    
    message_react(token, message_id, react_id)
    return dumps({})


@APP.route("/message/unreact", methods=['POST'])
def unreact_message():
    payload = request.get_json()
    token = payload['token']
    react_id = int(payload['react_id'])
    message_id = int(payload['message_id'])
    
    message_unreact(token, message_id, react_id)
    return dumps({})


@APP.route("/message/pin", methods=['POST'])
def pin_message():
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])

    message_pin(token, message_id)
    return dumps({})


@APP.route("/message/unpin", methods=['POST'])
def unpin_message():
    payload = request.get_json()
    token = payload['token']
    message_id = int(payload['message_id'])

    message_unpin(token, message_id)
    return dumps({})


#------------------standup methods----------------------------------#
@APP.route('/standup/start', methods=['POST'])
def start_standup():
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    length = int(payload['length'])

    response = dumps(standup_start(token, channel_id, length))
    return response


@APP.route('/standup/active', methods=['GET'])
def is_active_standup():
    payload = request.get_json()
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(standup_active(token, channel_id))


@APP.route('/standup/send', methods=['POST'])
def send_standup():
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
    return dumps(standup_send(token, channel_id, message))

@APP.route("/user/profile", methods=['GET'])
def return_profile():
    token = request.args.get('token') 
    u_id = request.args.get('u_id')
    return user_profile(token,u_id)

@APP.route("/user/profile/setname", methods=['PUT'])
def return_set_name():
    payload = request.get_json()
    token = payload['token']
    name_first = payload['name_first']
    name_last = payload['name_last']
    return user_profile_setname(token,name_first,name_last)

@APP.route("/user/profile/setemail", methods=['PUT'])
def return_set_email():
    payload = request.get_json()
    token = payload['token']
    email = payload['email']
    return user_profile_setemail(token,email)

@APP.route("/user/profile/sethandle", methods=['PUT'])
def return_set_handle():
    payload = request.get_json()
    token = payload['token']
    handle = payload['handle']
    return user_profile_sethandle(token,handle)

@APP.route("/users/all", methods=['GET'])
def return_all_users():
    token = request.args.get('token') 
    return users_all(token)

@APP.route("/search", methods=['GET'])
def return_message_search():
    token = request.args.get('token') 
    query_str = request.args.get('query_str')
    return search(token,query_str)

@APP.route('/workspace/reset', methods=['POST'])
def reset_workspace():
    return reset()

@APP.route('/userpermission/change', methods=['POST'])
def change_user_permission():
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']
    return change_permission(token,u_id,permission_id)

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8081))

