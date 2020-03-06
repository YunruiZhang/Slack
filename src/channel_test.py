import channel
import channels
import auth
import pytest
from error import InputError

def test_channel_invite():
    # Function channel_invite(token, channel_id, u_id)
    # Returns {}
    # Invites a user (with user id u_id) to join a channel with ID channel_id. Once invited the user is added to the channel immediately

    #Basic test with valid token, channel_id and u_id
        # channel_id = 1 (Type: Integer)
    u_id, token = auth.auth_login("example@email.com","password")
    user_channels = channels.channels_list(token)
    valid_channel_id = user_channels['channels'][0]['channel_id']
    assert channel.channel_invite(token, valid_channel_id, u_id) == {}
    
def test_channel_invite_except():
    # InputError:
    #   channel_id does not refer to a valid channel that the authorised user is part of.
    #   u_id does not refer to a valid user

    u_id, token = auth.auth_login("example@email.com","password")
    user_channels = channels.channels_list(token)
    all_channels = channels.channels_listall(token)
    valid_channel_id = user_channels['channels'][0]['channel_id']

    #Assuming 0 is an invalid _id and testing for type error

    with pytest.raises(InputError) as e:
        assert channel.channel_invite(token,0,u_id)
    with pytest.raises(InputError) as e:
        assert channel.channel_invite(token,"somestring",u_id)

    with pytest.raises(InputError) as e:
        assert channel.channel_invite(token,valid_channel_id,0)  
    with pytest.raises(InputError) as e:
        assert channel.channel_invite(token,valid_channel_id,"somestring")          

    # Access Error:
    #   The authorised user is not already a member of the channel
    
    #Find difference in list, hence giving us a list of channels that the user is not a member of
    difference_list = [i for i in all_channels["channels"] + user_channels["channels"] if i not in all_channels["channels"] or i not in user_channels["channels"]]

    #Assuming len(difference_list)>0 (In assumptions)
    if len(difference_list)>0 :
        with pytest.raises(AccessError) as e:
            assert channel.channel_invite(token, difference_list[0]['channel_id'], u_id)

def test_channel_details():
    # Function channel_details(token, channel_id)
    # Returns {name, owner_members, all_members}
    # Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel
    u_id, token = auth.auth_login("example@email.com","password")
    user_channels = channels.channels_list(token)
    valid_channel_id = user_channels['channels'][0]['channel_id']

    #Asserts that function returns a dictionary with keys ["name","owner_members","all_members"]
    assert list(channel.channel_details(token, valid_channel_id).keys()) == ["name","owner_members","all_members"]

def test_channel_details_except():

    u_id, token = auth.auth_login("example@email.com","password")
    user_channels = channels.channels_list(token)
    all_channels = channels.channels_listall(token)

    # InputError:
    #   Channel ID is not a valid channel
    # Assumption that 0 is an invalid _id and testing type error
    with pytest.raises(InputError) as e:
        assert channel.channel_details(token,0)
    with pytest.raises(InputError) as e:
        assert channel.channel_details(token,"somestring")

    # Access Error:
    #   Authorised user is not a member of channel with channel_id
    #Find difference in list, hence giving us a list of channels that the user is not a member of
    difference_list = [i for i in all_channels["channels"] + user_channels["channels"] if i not in all_channels["channels"] or i not in user_channels["channels"]]

    #Assuming len(difference_list)>0 (In assumptions)
    if len(difference_list)>0 :
        with pytest.raises(AccessError) as e:
            assert channel.channel_details(token, difference_list[0]['channel_id'])

def test_channel_messages():
    # Function channel_messages(token, channel_id, start)
    # Returns {messages, start, end}
    # Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.

    start = 0
    u_id, token = auth.auth_login("example@email.com","password")
    user_channels = channels.channels_list(token)
    valid_channel_id = user_channels['channels'][0]['channel_id']

    channel_msg = channel.channel_messages(token, valid_channel_id, start)

    assert list(channel_msg.keys()) == ['messages','start','end']
    assert channel_msg['end'] <= start+50 and channel_msg['end'] > -1

def test_channel_messages_except():

    u_id, token = auth.auth_login("example@email.com","password")
    user_channels = channels.channels_list(token)
    all_channels = channels.channels_listall(token)
    valid_channel_id = user_channels['channels'][0]['channel_id']
    # InputError:
    #   Channel ID is not a valid channel
    # Assumption that 0 is an invalid _id and testing type error
    with pytest.raises(InputError) as e:
        assert channel.channel_messages(token,0,0)
    with pytest.raises(InputError) as e:
        assert channel.channel_messages(token,"somestring",0)

    #   Start is greater than the total number of messages in the channel
    total_messages = len(channel.channel_messages(token,valid_channel_id,u_id)["messages"])

    with pytest.raises(InputError) as e:
        assert channel.channel_messages(token,valid_channel_id,total_messages+1)

    # Access Error:
    #   Authorised user is not a member of channel with channel_id
    #Find difference in list, hence giving us a list of channels that the user is not a member of
    difference_list = [i for i in all_channels["channels"] + user_channels["channels"] if i not in all_channels["channels"] or i not in user_channels["channels"]]

    #Assuming len(difference_list)>0 (In assumptions)
    if len(difference_list)>0 :
        with pytest.raises(AccessError) as e:
            assert channel.channel_messages(token, difference_list[0]['channel_id'], 0)


def test_channel_leave():
    # Function channel_leave(token, channel_id)
    # Returns {}
    # Given a channel ID, the user removed as a member of this channel
    u_id, token = auth.auth_login("example@email.com","password")
    user_channels = channels.channels_list(token)
    all_channels = channels.channels_listall(token)
    valid_channel_id = user_channels['channels'][0]['channel_id']

    assert channel.channel_leave(token,valid_channel_id) == {}

def test_channel_leave_except():
    # InputError:
    #   Channel ID is not a valid channel
    # Assumption that 0 is an invalid _id and testing type error
    u_id, token = auth.auth_login("example@email.com","password")
    with pytest.raises(InputError) as e:
        assert channel.channel_leave(token,0)
    with pytest.raises(InputError) as e:
        assert channel.channel_leave(token,"somestring")

    # Access Error:
    #   Authorised user is not a member of channel with channel_id
    #Find difference in list, hence giving us a list of channels that the user is not a member of
    difference_list = [i for i in all_channels["channels"] + user_channels["channels"] if i not in all_channels["channels"] or i not in user_channels["channels"]]

    #Assuming len(difference_list)>0 (In assumptions)
    if len(difference_list)>0 :
        with pytest.raises(AccessError) as e:
            assert channel.channel_leave(token, difference_list[0]['channel_id'])

def test_channel_join():
    # Function channel_join(token, channel_id)
    # Returns {}
    # Given a channel_id of a channel that the authorised user can join, adds them to that channel

    u_id, token = auth.auth_login("example@email.com","password")
    user_channels = channels.channels_list(token)
    all_channels = channels.channels_listall(token)

    channel_id_to_join = 1
    # Join a channel that the user is not already a member of
    difference_list = [i for i in all_channels["channels"] + user_channels["channels"] if i not in all_channels["channels"] or i not in user_channels["channels"]]
    if len(difference_list)>0:
        channel_id_to_join = difference_list[0]['channel_id']

    print(channel_id_to_join)

    assert channel.channel_join(token, channel_id_to_join) == {}

def test_channel_join_except():
    # InputError:
    #   Channel ID is not a valid channel
    u_id, token = auth.auth_login("example@email.com","password")
    user_channels = channels.channels_list(token)
    all_channels = channels.channels_listall(token)

    channel_id_to_join = 1
    # Join a channel that the user is not already a member of
    difference_list = [i for i in all_channels["channels"] + user_channels["channels"] if i not in all_channels["channels"] or i not in user_channels["channels"]]
    if len(difference_list)>0:
        channel_id_to_join = difference_list[0]['channel_id']

    with pytest.raises(InputError) as e:
        assert channel.channel_join(token,0)
    with pytest.raises(InputError) as e:
        assert channel.channel_join(token,"somestring")

    # Access Error:
    #   channel_id refers to a channel that is private (when the authorised user is not an admin)

    #Create a private channel
    priv_u_id, priv_token = auth.auth_login("private@email.com","private")
    private_channel = channels.channels_create(priv_token, "Private Channel", False)
    private_channel_id = private_channel['channel_id']

    with pytest.raises(AccessError) as e:
        assert channel.channel_join(token,private_channel_id)

def test_channel_addowner():
    # Function channel_addowner(token, channel_id, u_id)
    # Returns {}
    # Make user with user id u_id an owner of this channel
    u_id, token = get_user("user1")

    #Create a channel that the user is not a part of
    priv_u_id, priv_token = auth.auth_login("private@email.com","private")
    channel_to_join = channels.channels_create(priv_token, "Example Channel", True)
    channel_id_to_join = channel_to_join['channel_id']

    assert channel.channel_addowner(priv_token, channel_id_to_join, u_id) == {}

def test_channel_addowner_except():
    # InputError:
    #   Channel ID is not a valid channel
    u_id, token = get_user("user1")
    owner_id, owner_token = get_user("user2")

    # Create a channel with user's token, hence they are already the owner 
    channel_to_join = channels.channels_create(owner_token, "Example Channel", True)
    channel_id_to_join = channel_to_join['channel_id']

    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(owner_token,0,u_id)
    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(owner_token,"somestring",u_id)

    #   When user with user id u_id is already an owner of the channel
    with pytest.raises(InputError) as e:
        assert channel.channel_addowner(owner_token,channel_id_to_join,owner_id)

    # Access Error:
    #   The authorised user is not an owner of the slackr, or an owner of this channel
    # Create a private user, who is not an owner of the previously made channel "Example Channel" 
    not_owner_id, not_owner_token = get_user("user3")

    with pytest.raises(AccessError) as e:
        assert channel.channel_addowner(not_owner_token,channel_id_to_join,u_id)

def test_channel_removeowner():
    # Function channel_addowner(token, channel_id, u_id)
    # Returns {}
    # Remove user with user id u_id an owner of this channel

    # Make user with user id u_id an owner of this channel
    u_id, token = get_user("user1")
    u_id_2, token_2 = get_user("user2")

    channel_to_remove = channels.channels_create(token, "Example Channel", True)
    channel_id_to_remove = channel_to_remove["channel_id"]
    channel.channel_addowner(token, channel_id_to_remove,u_id_2)
    assert channel.channel_removeowner(token, channel_id_to_remove, u_id_2) == {}

def test_channel_removeowner_except():
    # InputError:
    #   Channel ID is not a valid channel
    u_id, token = get_user("user1")
    owner_id, owner_token = get_user("user2")
    # Create a channel with user's token, hence they are already the owner 
    channel_to_remove = channels.channels_create(owner_token, "Example Channel", True)
    channel_id_to_remove = channel_to_remove['channel_id']

    with pytest.raises(InputError) as e:
        assert channel.channel_removeowner(owner_token,0,u_id)
    with pytest.raises(InputError) as e:
        assert channel.channel_removeowner(owner_token,"somestring",u_id)

    #   When user with user id u_id is not an owner of the channel
    with pytest.raises(InputError) as e:
        assert channel.channel_removeowner(owner_token, channel_id_to_remove, u_id)
    
    # Access Error:
    #   The authorised user is not an owner of the slackr, or an owner of this channel
    with pytest.raises(AccessError) as e:
        assert channel.channel_removeowner(token,channel_id_to_remove,owner_id)


#def test_channels_list():
    # Function channels_list(token)
    # Returns {channels}
    # Provide a list of all channels (and their associated details) that the authorised user is part of

#def test_channels_listall():
    # Function channels_listall(token)
    # Returns {channels}
    # Provide a list of all channels (and their associated details)

#def test_channels_create():
    # Function channels_create(token, name, is_public)  
    # Returns {channel_id}
    # Creates a new channel with that name that is either a public or private channel

#def test_channels_create_except():
    # InputError:
    #   Name is more than 20 characters long

def get_user(username):
    auth.auth_register(username+"@email.com", username+"pass", "John", "Doe")
    return auth.auth_login("example@email.com","password")

