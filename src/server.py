import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from channel import *
from channels import *

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

    auth_data = auth.auth_logout(data['token'])

    return dumps({
        'is_success': auth_data['is_success'],
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
        'u_id': ,
        'token': ,
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
    token = payload['token']#request.form.get('token')
    channel_id = payload['channel_id']#request.form.get('channel_id')
    return channel_leave(token, channel_id)

@APP.route("/channel/join", methods=['POST'])
def return_channel_join():
    payload = request.get_json()
    token = payload['token']#request.form.get('token')
    channel_id = payload['channel_id']#request.form.get('channel_id')
    return channel_join(token,channel_id)

@APP.route("/channel/addowner", methods=['POST'])
def return_channel_addowner():
    payload = request.get_json()
    token = payload['token']#request.form.get('token')
    channel_id = payload['channel_id']#request.form.get('channel_id')
    u_id = payload['u_id']
    return channel_addowner(token,channel_id,u_id)

@APP.route("/channel/removeowner", methods=['POST'])
def return_channel_removeowner():
    payload = request.get_json()
    token = payload['token']#request.form.get('token')
    channel_id = payload['channel_id']#request.form.get('channel_id')
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
    token = payload['token']#request.form.get('token')
    name = payload['name']#request.form.get('name')
    is_public = payload['is_public']#request.form.get('is_public')    
    return channels_create(token,name,is_public) 


if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))

