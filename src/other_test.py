import other
import auth
import message
import channels
from database import *

#------------------------------------------test the users_all function---------------------------------#
def test_users_all():
    reset()
    query_str = 'world'
    person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')

    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    assert other.users_all(login_person1['token']) == {'users':[{
        'u_id': 1,
        'email': 'cs1531@cse.unsw.edu.au',
        'name_first': 'Hayden',
        'name_last': 'Jacobs',
        'handle_str': 'haydenjacobs',
    }
                                                               ]}

#------------------------------------------test the search function---------------------------------#

def test_search():
    reset()
    query_str = 'world'
    person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')
    #person2 = auth.auth_register('cs1532@cse.unsw.edu.au', 'abc1234', 'Mayden', 'Hacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', "abc123")
    person1_u_id = login_person1['u_id']
    person1_token = login_person1['token']
    new_Channel = channels.channels_create(person1_token, 'Channel 1', True)
    message1_id = message.message_send(person1_token, new_Channel['channel_id'], 'Hello world')['message_id']

    message1_collection = other.search(person1_token, query_str)

    assert message1_collection['messages'][0]['message_id'] == 1
    assert message1_collection['messages'][0]['u_id'] == 1
    assert message1_collection['messages'][0]['message'] == 'Hello world'
