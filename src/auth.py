'''
This file contains information about authorizing a user.  The methods in this
file relate to registering, loging in and loging out for a user.  There is a helper
method called valid_email that is used to validate emails that are entered by the
user.
'''
import random
import re
import smtplib
import zlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from error import InputError
from database import *

def valid_email(email):
    '''
    Returns whether the given email is valid

    Parameters:
        email (str): User's Email

    Returns:
        (bool): Whether the email is valid
    '''
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if re.search(regex, email):
        return True
    return False


def auth_login(email, password):
    '''
    Takes an email and password and logs the user into their
    account if the given information is valid.  Will throw
    errors with incorrect information

    Parameters:
        email (str): User's Email
        password (str): User's Password

    Returns:
        dict {
            u_id (str): The user's id corresponding to their account
            token (str): A token generated for the session
        }
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

    Parameters:
        token (str): token generated for the user's session

    Returns:
        dict {
            is_success (bool): if the user successfully logged out
        }
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
    This method registers a new user based on the parameters given and
    checks if the new information of the user in the database.  Also,
    it checks if the credentials entered fit the specs and a current
    user is not trying to re-register

    Parameters:
        email (str): User's email
        password (str): User's password
        name_first (str): User's first name
        name_last (str): User's last name

    Returns:
        dict {
            u_id (str): The user's id corresponding to their account
            token (str): A token generated for the session
        }
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
            raise InputError("Error, email: is already in use")


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
    '''
    Request's the user's email when trying to reset the
    user's password

    Parameters:
        email (str): User's email

    Returns:
        (dict): Empty dictionary
    '''
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
    return {}

def password_reset(reset_code, new_password):
    '''
    Reset's the user's password in the case that they forgot
    their original one

    Parameters:
        reset_code (str): Code received from password request method
        new_password (str): New password that the user wants to reset their password with

    Returns:
        (dict): Empty dictionary
    '''
    code = unobscure(reset_code).decode('utf-8')

    email, old_password = code[:code.find("|")], code[code.find("|")+1:]
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
