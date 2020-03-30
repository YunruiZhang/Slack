import urllib
import json
import datetime
from server import *

# set up

URL = 'http://127.0.0.1:8081'
email = '1234@gmail.com'
password = 'qwertyu1234'
name_first = 'FIRSTNAME'
name_last = 'LASTNAME'

# POST: /standup/start
def test_standup_start():

    req = urllib.request.Request(f"{URL}/workspace/reset", data={}, headers={'Content-Type': 'application/json'})
    json.load(urllib.request.urlopen(req))

    data = json.dumps({
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    }).encode('utf-8')

    req = urllib.request.Request(f"{URL}/auth/register", data=data, headers={'Content-Type': 'application/json'}, method='POST')
    response = json.load(urllib.request.urlopen(req))

    u_id = response['u_id']
    #To comply with pylint
    u_id = u_id
    token = response['token']

    create_data = json.dumps({
        "token" : token,
        "name" : "CHANNEL_1",
        "is_public" : True
    }).encode('utf-8')

    req = urllib.request.Request(f"{URL}/channels/create", data=create_data, headers={'Content-Type': 'application/json'})
    channel_id_to_invite = json.load(urllib.request.urlopen(req))

    channel_id = channel_id_to_invite['channel_id']

    length = 10
    current_time = datetime.datetime.utcnow().replace(tzinfo=timezone('UTC')).timestamp()
    time_finish = current_time + length

    data = json.dumps({
        'token':token,
        'channel_id':channel_id,
        'length':length
    }).encode('utf-8')

    req = urllib.request.Request(f"{URL}/standup/start", data=data, headers={'Content-Type':'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    #ch = get_channel_from_channelID(channel_id)
    #time_finish_stored = ch['standup']['time_finish']
    #Hard to get exact time, so approx (Within a second)
    assert round(payload['time_finish']) == round(time_finish)

    # Stand_up start only returns time_finish so no need/can't check:
    #assert ch['standup']['is_active'] == True

    # GET: /standup/active

    payload = json.load(urllib.request.urlopen(f"{URL}/standup/active?token={token}&channel_id={channel_id}"))
    assert payload['is_active']
    #assert payload['time_finish'] == ch['standup']['time_finish']

    # POST: /standup/send
    data = json.dumps({
        'token':token,
        'channel_id':channel_id,
        'message':"PENDING_MSG"
    }).encode('utf-8')
    print(data)
    req = urllib.request.Request(f"{URL}/standup/send", data=data, headers={'Content-Type':'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    assert payload == {}
