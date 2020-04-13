'''
This file contains information about authorizing a user.  The methods in this
file relate to registering, loging in and loging out for a user.  There is a helper
method called valid_email that is used to validate emails that are entered by the
user.
'''
import random
import re
from database import *
from error import InputError, AccessError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

def valid_email(email):
    '''
    This method checks that the email given is valid
    '''
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if re.search(regex, email):
        return True
    return False


def auth_login(email, password):
    '''
    This method takes in a user's email and password and checks to see
    if they are registered.  If so, then the user will be granted a token
    and be able to login.  Otherwise, errors will be raised.
    '''

    #Get the Database
    store = getData()

    #Checks that the email entered is valid
    if not valid_email(email):
        raise InputError("Email entered is not a valid email address")

    #Iterate through the database over the email to make sure
    #that there is a matching email and then check to see if the
    #password matches the email account.  Then return the user's
    #u_id along with a new token

    for users in store['users']:
        if users['email'] == email:
            if users['password'] == str(obscure(password.encode('utf-8'))):
                return {
                    'u_id': users['u_id'],
                    'token': token_generate(users['u_id'])
                }
            else:
                raise InputError("Password is not correct")

    #If the code has gotten to this point, raise InputError since
    #the given email did not match any in the database
    raise InputError("Email entered does not belong to a user")

def auth_logout(token):
    '''
    This method will look out a user given a valid token.  The output
    is a dictionary that states wether the method call was a sucess or
    not
    '''

    #Must check if the token is in the database to prevent a double
    #logout

    store = getData()
    token_is_being_used = False

    for users in store['users']:
        if users['token'] == token:
            token_is_being_used = True

    if not verify_token(token) or not token_is_being_used:
        return {
            'is_success': False,
        }
    for users in store['users']:
        if users['token'] == token:
            users['token'] = ""

    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    '''
    This method registers a new user based on the parameters given.  The
    output of this method returns the u_id and token to allow the user
    to continue with their session, although it is important to save the
    new information of the user in the database.  Also, we must check to see
    if the credentials entered fit the specs and a current user is not trying
    to re-register
    '''

    store = getData()

    #Gets the first and last name to make a u_id but if it is longer than
    #20 characters the u_id will cutoff at the 20 chars count
    #login = name_first + name_last
    #u_id = (login[:20]) if len(login) > 20 else login

    login = name_first.lower().replace(" ", "") + name_last.lower().replace(" ", "")
    handle = (login[:20]) if len(login) > 20 else login

    for users in store['users']:
        if users['handle_str'] == handle:
            handle = handle[:19] + str(random.randint(0, 9))

    if store['users']:
        u_id = store['users'][-1]['u_id'] + 1
    else:
        u_id = 1

    #Checks if the email entered is valid
    if not valid_email(email):
        raise InputError("Email entered is not a valid email address")

    #Will check to see if there u_id created is unique and if it
    #is not, it will add a one to the name to make it unique.  It
    #will also check if the email that was inputed is currently being
    #used by a user in the database

    for users in store['users']:
        if users['email'] == email:
            raise InputError(f"Error, email: {email} is already in use")


    #Checks if password is Valid
    if len(password) < 6:
        raise InputError("Password is too short")

    #Checks if name_first are Valid
    if not 1 <= len(name_first) <= 50:
        raise InputError("First name is not valid")

    #Checks if name_last are Valid
    if not 1 <= len(name_last) <= 50:
        raise InputError("Last name is not valid")

    #Creating a token
    token = token_generate(u_id)

    if store['users']:
        permission_id = 2
    else:
        permission_id = 1

    #Creating the user and putting it in the database
    create_user(u_id, permission_id, handle, token, email, str(obscure(password.encode('utf-8'))), name_first, name_last)


    return {
        'u_id': u_id,
        'token': token,
    }

def password_request(email):
    data = getData()

    for users in data["users"]:
        if users["email"] == email:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login("T18AWELV", "t18awelv")

                msg = MIMEMultipart()
                msg['From'] = "Slackr"
                msg['To'] = users["name_first"]
                msg['Subject'] = "Slackr email reset"

                secret_code = obscure(email.encode('utf-8')+"|".encode('utf-8')+(str(users["password"])).encode('utf-8'))
                body = "Your secret code is: " + secret_code.decode('utf-8') # The /n separates the message from the headers
                msg.attach(MIMEText(body, 'plain'))
                server.sendmail("T18AWELV@gmail.com", email, msg.as_string())
                return {}
                break

def password_reset(reset_code, new_password):
    code = unobscure(reset_code).decode('utf-8')

    email,old_password = code[:code.find("|")],code[code.find("|")+1:]
    data = getData()

    if len(new_password) < 6:
        raise InputError("Password is too short")

    for users in data["users"]:
        if users["email"] == email:
            if users["password"] == old_password:  
                users["password"] = str(obscure(new_password.encode('utf-8')))
                update_database(data)
                return {}

    raise InputError("Reset code invalid")

def obscure(data: bytes) -> bytes:
    return b64e(zlib.compress(data, 9))

def unobscure(obscured: bytes) -> bytes:
    return zlib.decompress(b64d(obscured))

