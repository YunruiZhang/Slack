import channel
import channels
import auth
import pytest
from other import *
from database import *
from error import InputError, AccessError
from urllib.error import HTTPError
import json
import urllib
import flask 
import sys

BASE_URL = 'http://127.0.0.1:8081'

def test_channel_invite():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    u_id, token = get_user("user1")
    owner_id, owner_token = get_user("user2")
    channel_id = create_channel(token,"Example Channel",1,1)
    # Function channel_join(token, channel_id)
    # Returns {}
    # Given a channel_id of a channel that the authorised user can join, adds them to that channel
    data = json.dumps({
        "token" : owner_token,
        "channel_id" : channel_id
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channel/join", data=data,headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    
    #urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})

    assert payload == {}

def test_channel_invite_except():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    u_id, token = get_user("user1")
    owner_id, owner_token = get_user("user2")
    random_id, random_token = get_user("user3")
    
    channel_id_to_invite = create_channel(owner_token,"Example Channel",1,1)

    # InputError:
    #   channel_id does not refer to a valid channel that the authorised user is part of.
    #Assuming 0 is an invalid _id 

    data = json.dumps({
        'token': owner_token,
        'channel_id': 0,
        'u_id' : u_id 
    }).encode('utf-8')

    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data, headers={'Content-Type': 'application/json'})
        json.load(urllib.request.urlopen(req))
   
    #   u_id does not refer to a valid user

    data = json.dumps({
        'token': owner_token,
        'channel_id': channel_id_to_invite,
        'u_id' : 0 
    }).encode('utf-8')

    print(getData()['users'])

    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data, headers={'Content-Type': 'application/json'})
        json.load(urllib.request.urlopen(req))

    # Access Error:
    #   The authorised user is not already a member of the channel

    data = json.dumps({
        'token': random_token,
        'channel_id': channel_id_to_invite,
        'u_id' : u_id 
    }).encode('utf-8')

    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data, headers={'Content-Type': 'application/json'})
        json.load(urllib.request.urlopen(req))


def test_channel_details():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))
    # Function channel_details(token, channel_id)
    # Returns {name, owner_members, all_members}
    # Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel
    u_id, token = get_user("user1")
    channel_id = create_channel(token,"Example Channel",1,1)
    
    response = urllib.request.urlopen(f'{BASE_URL}/channel/details?token={token}&channel_id={channel_id}')
    payload = json.load(response)

    #Asserts that function returns a dictionary with keys ["name","owner_members","all_members"]
    list_of_keys = payload.keys()
    assert 'name' in list_of_keys 
    assert 'owner_members' in list_of_keys
    assert 'all_members' in list_of_keys

def test_channel_details_except():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))
    u_id, token = get_user("user1")
    channel_id = create_channel(token,"Example Channel",1,1)

    # InputError:
    #   Channel ID is not a valid channel
    # Assumption that 0 is an invalid _id and testing type error
    with pytest.raises(HTTPError) as e:
        response = urllib.request.urlopen(f'{BASE_URL}/channel/details?token={token}&channel_id=0')

    # Access Error:
    #   Authorised user is not a member of channel with channel_id
    new_id, new_token = get_user("user2")

    with pytest.raises(HTTPError) as e:
        response = urllib.request.urlopen(f'{BASE_URL}/channel/details?token={new_token}&channel_id={channel_id}')

def test_channel_messages():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    # Function channel_messages(token, channel_id, start)
    # Returns {messages, start, end}
    # Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.

    start = 0
    u_id, token = get_user("user1")
    channel_id = create_channel(token,"Example Channel",1,1)

    response = urllib.request.urlopen(f'{BASE_URL}/channel/messages?token={token}&channel_id={channel_id}&start={start}')
    payload = json.load(response)

    list_of_keys = payload.keys()
    assert 'messages' in list_of_keys 
    assert 'start' in list_of_keys
    assert 'end' in list_of_keys
    
    assert payload['end'] <= start+50 or payload['end'] > -1

def test_channel_messages_except():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    u_id, token = get_user("user1")
    channel_id = create_channel(token,"Example Channel",1,1)
    # InputError:
    #   Channel ID is not a valid channel
    # Assumption that 0 is an invalid _id and testing type error
    with pytest.raises(HTTPError) as e:
        response = urllib.request.urlopen(f'{BASE_URL}/channel/messages?token={token}&channel_id=0&start=0')

    #   Start is greater than the total number of messages in the channel
    # Assuming that the list "messages" contains all the messages in the channel
    max_int = sys.maxsize   

    with pytest.raises(HTTPError) as e:
        response = urllib.request.urlopen(f'{BASE_URL}/channel/messages?token={token}&channel_id={channel_id}&start={max_int}')

    # Access Error:
    #   Authorised user is not a member of channel with channel_id
    # Create a new user, who is not a member of channel with channel_id
    random_id, random_token = get_user("user2")
    with pytest.raises(HTTPError) as e:
        response = urllib.request.urlopen(f'{BASE_URL}/channel/messages?token={random_token}&channel_id={channel_id}&start={max_int}')


def test_channel_leave():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    # Function channel_leave(token, channel_id)
    # Returns {}
    # Given a channel ID, the user removed as a member of this channel
    u_id, token = get_user("user1")
    channel_id = create_channel(token,"Example Channel",1,1)

    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channel/leave", data=data,headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    assert payload == {}

def test_channel_leave_except():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    u_id, token = get_user("user1")
    channel_id = create_channel(token,"Example Channel",1,1)
    # InputError:
    #   Channel ID is not a valid channel
    # Assumption that 0 is an invalid _id and testing type error

    data = json.dumps({
        "token" : token,
        "channel_id" : 0
    }).encode('utf-8')

    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/leave", data=data,headers={'Content-Type': 'application/json'})
        payload = json.load(urllib.request.urlopen(req))
 
    # Access Error:
    #   Authorised user is not a member of channel with channel_id
    random_id, random_token = get_user("user2")
    
    data = json.dumps({
        "token" : random_token,
        "channel_id" : channel_id
    }).encode('utf-8')

    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/leave", data=data,headers={'Content-Type': 'application/json'})
        payload = json.load(urllib.request.urlopen(req))

def test_channel_join():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    u_id, token = get_user("user1")
    channel_id = create_channel(token,"Example Channel",1,1)
    # Function channel_join(token, channel_id)
    # Returns {}
    # Given a channel_id of a channel that the authorised user can join, adds them to that channel
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channel/join", data=data,headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    
    assert payload == {}

def test_channel_join_except():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    u_id, token = get_user("user1")
    channel_id = create_channel(token,"Example Channel",1,1)
    # InputError:
    #   Channel ID is not a valid channel
    data = json.dumps({
        "token" : token,
        "channel_id" : 0
    }).encode('utf-8')

    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/join", data=data,headers={'Content-Type': 'application/json'})
        payload = json.load(urllib.request.urlopen(req))
    
    # Access Error:
    #   channel_id refers to a channel that is private (when the authorised user is not an admin)
    #Create a private channel
    owner_u_id, owner_token = get_user("user2")
    private_channel_id = create_channel(owner_token,"Private Channel",0,1)

    # Try to get new user to join when they are not admin/owner
    data = json.dumps({
        "token" : token,
        "channel_id" : private_channel_id
    }).encode('utf-8')

    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/join", data=data,headers={'Content-Type': 'application/json'})
        payload = json.load(urllib.request.urlopen(req))

def test_channel_addowner():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    # Function channel_addowner(token, channel_id, u_id)
    # Returns {}
    # Make user with user id u_id an owner of this channel
    u_id, token = get_user("user1")
    new_id, new_token = get_user("user2")
    channel_id = create_channel(token,"Example Channel",1,1)

    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
        "u_id": new_id
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data,headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    assert payload == {}

def test_channel_addowner_except():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    # InputError:
    #   Channel ID is not a valid channel
    u_id, token = get_user("user1")
    owner_id, owner_token = get_user("user2")

    # Create a channel with user's token, hence they are already the owner 
    channel_id = create_channel(token,"Example Channel",1,1)

    data = json.dumps({
        "token" : owner_token,
        "channel_id" : 0,
        "u_id": u_id
    }).encode('utf-8')
    
    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data,headers={'Content-Type': 'application/json'})
        payload = json.load(urllib.request.urlopen(req))

    #   When user with user id u_id is already an owner of the channel

    data = json.dumps({
        "token" : owner_token,
        "channel_id" : channel_id,
        "u_id": owner_id
    }).encode('utf-8')

    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data,headers={'Content-Type': 'application/json'})
        payload = json.load(urllib.request.urlopen(req))

    # Access Error:
    #   The authorised user is not an owner of the slackr, or an owner of this channel
    # Create a private user, who is not an owner of the previously made channel "Example Channel" 
    not_owner_id, not_owner_token = get_user("user3")
    data = json.dumps({
        "token" : not_owner_token,
        "channel_id" : channel_id,
        "u_id": u_id
    }).encode('utf-8')

    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data,headers={'Content-Type': 'application/json'})
        payload = json.load(urllib.request.urlopen(req))

def test_channel_removeowner():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    # Function channel_addowner(token, channel_id, u_id)
    # Returns {}
    # Remove user with user id u_id an owner of this channel

    # Make user with user id u_id an owner of this channel
    u_id, token = get_user("user1")
    new_id, new_token = get_user("user2")
    channel_id = create_channel(token,"Example Channel",1,1)
    # Add new user as owner
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
        "u_id": new_id
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data,headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    # Remove them immediately (Whoops)
    req = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data,headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    assert payload == {}

def test_channel_removeowner_except():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    u_id, token = get_user("user1")
    owner_id, owner_token = get_user("user2")
    # InputError:
    #   Channel ID is not a valid channel
    # Create a channel with user's token, hence they are already the owner 
    channel_id = create_channel(owner_token,"Example Channel",1,1)

    data = json.dumps({
        "token" : owner_token,
        "channel_id" : 0,
        "u_id": owner_id
    }).encode('utf-8')

    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data,headers={'Content-Type': 'application/json'})
        payload = json.load(urllib.request.urlopen(req))

    #   When user with user id u_id is not an owner of the channel
    data = json.dumps({
        "token" : owner_token,
        "channel_id" : channel_id,
        "u_id": u_id
    }).encode('utf-8')

    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data,headers={'Content-Type': 'application/json'})
        payload = json.load(urllib.request.urlopen(req))
    
    # Access Error:
    #   The authorised user is not an owner of the slackr, or an owner of this channel
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
        "u_id": u_id
    }).encode('utf-8')

    with pytest.raises(HTTPError) as e:
        req = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data,headers={'Content-Type': 'application/json'})
        payload = json.load(urllib.request.urlopen(req))

def test_channels_list():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    # Function channels_list(token)
    # Returns {channels}
    # Provide a list of all channels (and their associated details) that the authorised user is part of

    u_id, token = get_user("user1")

    response = urllib.request.urlopen(f'{BASE_URL}/channels/list?token={token}')
    payload = json.load(response)
    #Assert that function returns a dictionary with keys "channels"
    assert payload.keys() == {"channels"}

def test_channels_listall():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    # Function channels_listall(token)
    # Returns {channels}
    # Provide a list of all channels (and their associated details)

    u_id, token = get_user("user1")
    response = urllib.request.urlopen(f'{BASE_URL}/channels/listall?token={token}')
    payload = json.load(response)
    #Assert that function returns a dictionary with keys "channels"
    assert payload.keys() == {"channels"}

def test_channels_create():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    # Function channels_create(token, name, is_public)  
    # Returns {channel_id}
    # Creates a new channel with that name that is either a public or private channel

    u_id, token = get_user("user1")
    #Assert that function returns a dictionary with keys "channel_id"

    assert create_channel(token,"Example Channel",1,False).keys() == {"channel_id"}
    assert create_channel(token,"Example Channel",0,False).keys() == {"channel_id"}

def test_channels_create_except():
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset",data={},headers={'Content-Type': 'application/json'})    
    json.load(urllib.request.urlopen(req))

    # InputError:
    #   Name is more than 20 characters long
    u_id, token = get_user("user1")
    #Assert that function returns a dictionary with keys "channel_id"
    with pytest.raises(HTTPError) as e:
        channel_id =  create_channel(token,"Example Channel with a ridiculiously long name",0,1)

def get_user(username):
    #response = auth.auth_register(username+"@email.com", "password123", "John", "Doe")

    data = json.dumps({
        'email': username+'@email.com',
        'password': '123password',
        'name_first': 'John',
        'name_last': 'Doe'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/register",data=data,headers={'Content-Type': 'application/json'}, method='POST')
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    return (payload['u_id'],payload['token'])
    # Can use this otherwise
    #return auth.auth_login("example@email.com","password")

    # Use this if auth functions aren't implemented
    '''
    DATA = getData()

    DATA['users'].append( {'u_id' : int(username[-1]),
            'name_first': "example first", 
            'name_last': "example last", 
            'password': "badpassword", 
            'handle': 'hayden',
            'email': "email@example.com"
            })

    return(int(username[-1]), token_generate(int(username[-1])))
    '''
def create_channel(token,name,public,return_id):

    create_data = json.dumps({
        "token" : token,
        "name" : name,
        "is_public" : public
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=create_data,headers={'Content-Type': 'application/json'})
    channel_id_to_invite = json.load(urllib.request.urlopen(req))

    if return_id:
        return channel_id_to_invite['channel_id']
    else:
        return channel_id_to_invite