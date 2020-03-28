def users_all(token):
    all_user = []
    Data = getdata()
    
    operate_u_id = verify_token(token)
    if not operate_u_id:
        raise AccessError('Token Invalid')
    for user in Data['users']:
        all_user.append(user)
    
    return{ 'list' : all_user }
   
''' return {
        'users': [
            {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
            },
        ],
    }'''

def search(token, query_str):
    search_message = []
    Data = getdata()
    
    for single_message in Data['messages']:
        if query_str in single_message['message']:
            i = 0
            if search_message == []:
                search_message[0] = single_message
            else:
                while(i < len(single_message)):
                    time_origin = search_message[i]['time_created']
                    if single_message['time_created'] > time_origin:
                        search_message[1] = search_message[0]
                        search_message[0] = single_message
                        break
                    else:
                        i = i + 1
    
    return { 'messages' : search_message }
    
    
    '''return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }'''
