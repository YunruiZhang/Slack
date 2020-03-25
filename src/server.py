import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import message
import database

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


@APP.route("/message/send", methods = ['POST'])
def message_send():
    jason = request.get_json()
    msg_id = message.message_send(jason['token'], jason['channel_id'], jason['message'])
    return dumps(msgid)

@APP.route("/message/remove", methods = ['DELETE'])
def message_remove():
    jason = request.get_json()
    message.message_remove(jason['token'], jason['message_id'])
    return dumps()

@APP.route("message/edit", methods = ['PUT'])
def message_edit():
    jason = request.get_json()
    message.message_edit(jason[token], jason['message_id'], jason['message'])
    return dumps()

@APP.route("message/sendlater", methods = ['POST'])
def message_sendlater():
    jason= request.get_json()
    message.message_sendlater(jason['token'], jason['channel_id'], jason['message'], jason['time_sent'])
# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
