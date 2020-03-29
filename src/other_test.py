import other,auth,message,channel,channels
from database import *
import pytest
query_str = 'world'
person1 = auth.auth_register('cs1531@cse.unsw.edu.au', 'abc123', 'Hayden', 'Jacobs')


#------------------------------------------test the users_all function---------------------------------#
def test_users_all():
    
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', 'abc123')
    assert other.users_all(login_person1['token']) == [{
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle': 'haydenjacobs',
            }
        ]




#------------------------------------------test the search function---------------------------------#    
def test_search():
   
    #person2 = auth.auth_register('cs1532@cse.unsw.edu.au', 'abc1234', 'Mayden', 'Hacobs')
    login_person1 = auth.auth_login('cs1531@cse.unsw.edu.au', "abc123")
    person1_u_id = login_person1['u_id']
    person1_token = login_person1['token']
    new_Channel = channels.channels_create(person1_token, 'Channel 1', True)
    message1_id = message.message_send(person1_token, new_Channel, 'Hello world')['message_id']

    assert other.search(person1_token, query_str) == { 'messages': [
            {
                'message_id':message1_id,
                'u_id': person1_u_id,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
