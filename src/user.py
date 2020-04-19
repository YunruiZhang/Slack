'''
This file contains information about anything relating to the user.  The 
methods in this file relate to getting the users details and editing said
details (This includes the profile picture).  There are some helper methods 
that just check the existence of channels and users.
'''
import re
import pathlib
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from os.path import splitext, basename
from flask import url_for
from PIL import Image
from database import *
from channel import *
from error import *

def user_profile(token, u_id):
    '''
    The details of a user

    Parameters:
        token (str): Generated token from user's login session
        u_id (str): User's id

    Returns:
        dict{
            u_id (str): User's id
            email (str): The user's email
            name_first (str): The user's first name
            name_last (str): The User's last name
            handle_str (str): The user's handle
            profile_img_url (str): The url of a user's profile pic
        }
    '''
    DATA = getData()

    if not verify_token(token):
        raise AccessError('Invalid Token')

    foundFlag = False
    for users in DATA['users']:
        if int(users['u_id']) == int(u_id):
            foundFlag = True
            break

    if not foundFlag:
        raise InputError('Invalid User ID')

    return_user = {
        'u_id' : users['u_id'],
        'email' : users['email'],
        'name_first' : users['name_first'],
        'name_last' : users['name_last'],
        'handle_str' : users['handle_str'],
        'profile_img_url': users['profile_img_url']
    }
    update_database(DATA)
    return return_user

def user_profile_setname(token, name_first, name_last):
    '''
    Setting the name of a user

    Parameters:
        token (str): Generated token from user's login session
        name_first (str): User's first name
        name_last (str): User's last name

    Returns:
        (dict): emtpy dictionary
    '''
    Data = getData()

    if not user_name_length_check(name_first):
        raise InputError('Length of first name is invalid')

    if not user_name_length_check(name_last):
        raise InputError('Length of last name is invalid')

    curr_u_id = verify_token(token)

    for user in Data['users']:
        if int(user['u_id']) == int(curr_u_id):
            user['name_first'] = name_first
            user['name_last'] = name_last
            break
    update_database(Data)
    return {
    }

def user_profile_setemail(token, email):
    '''
    Setting the email of a user

    Parameters:
        token (str): Generated token from user's login session
        email (str): User's new email

    Returns:
        (dict): emtpy dictionary
    '''
    Data = getData()

    if not user_email_check(email):
        raise InputError('Email has already been used')

    if not check(email):
        raise InputError("Email entered is not a valid email address")

    curr_u_id = verify_token(token)
   # if not curr_u_id:
    #    raise AccessError('Token Invalid')

    for user in Data['users']:
        if int(user['u_id']) == int(curr_u_id):
            break

    user['email'] = email
    update_database(Data)
    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    Setting the handle of a user

    Parameters:
        token (str): Generated token from user's login session
        handle_str (str): User's handle

    Returns:
        (dict): emtpy dictionary
    '''
    DATA = getData()

    if not user_handle_length_check(handle_str):
        raise InputError('Length of handle is invalid')

    if not user_handle_check(handle_str):
        raise InputError('Handle has already been used')

    curr_u_id = verify_token(token)
   # if not curr_u_id:
   #     raise AccessError('Token Invalid')

    for user in DATA['users']:
        if int(user['u_id']) == int(curr_u_id):
            break

    user['handle_str'] = handle_str
    update_database(DATA)
    return {
    }

def profile_picture(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Setting the profile pic for a user

    Parameters:
        token (str): Generated token from user's login session
        img_url (str):  Image url in str format
        x_start (int): X cord of image
        y_start (int): Y cord of image
        x_end (int): X cord end of image
        y_end (int): Y cord end of image

    Returns:
        (dict): emtpy dictionary
    '''
    DATA = getData()

    disassembled = urlparse(img_url)
    filename, file_ext = splitext(basename(disassembled.path))

    req = Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
    image_file = Image.open(urlopen(req))
    #image_file = io.BytesIO(fd.read())

    #if not fd:
    #    raise InputError("Image URL invalid")

    #if image_file.what(image_file) != "jpeg":
    #    raise InputError("Not a JPG file")

    width, height = image_file.size
    print(f"filename: {filename}")
    if int(x_start) < 0 or int(y_start) < 0:
        raise InputError("Coordinates not within the bounds of the image")

    if int(x_end)-int(x_start) > width or int(y_end) - int(y_start) > height:
        raise InputError("Coordinates not within the bounds of the image")

    cropped_image = image_file.crop((int(x_start), int(y_start), int(x_end), int(y_end)))
    u_id = verify_token(token)

    cropped_image.save(pathlib.Path(str(pathlib.Path().absolute())+"/static/"+filename+".jpg"))
    cropped_image.show()

    img_path = filename+".jpg"
    default_pic = url_for('static', filename=img_path, _external=True)

    for users in DATA["users"]:
        if users["u_id"] == int(u_id):
            users["profile_img_url"] = default_pic
            break

    update_database(DATA)

    return {}

def user_email_check(email):
    '''
    Helper method that checks for the email in the database

    Parameters:
        email (str): User's email

    Returns:
        (bool): returns True if the email is in the database
    '''
    DATA = getData()
    for users in DATA['users']:
        if users['email'] == email:
            return False
    return True

def user_handle_check(handle):
    '''
    Helper method that checks for a handle

    Parameters:
        handle (str): User's handle

    Returns:
        (bool): returns True if the handle is in the database
    '''
    DATA = getData()
    for users in DATA['users']:
        if users['handle_str'] == handle:
            return False
    return True

def user_name_length_check(name):
    '''
    Helper method that checks the length of a name

    Parameters:
        name (str): User's name

    Returns:
        (bool): returns True if the name is valid
    '''
    if not name or len(name) > 50:
        return False
    return True

def user_handle_length_check(handle):
    '''
    Helper method that checks the length of a handle

    Parameters:
        handle (str): User's handle

    Returns:
        (bool): returns True if the name is valid length
    '''
    if len(handle) < 2 or len(handle) > 20:
        return False
    return True

# Make a regular expression
# for validating an Email
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

# Define a function for
# for validating an Email
def check(email):
    '''
    Helper method that checks the validity of an email address

    Parameters:
        email (str): User's email

    Returns:
        (bool): returns True if the name is email is valid
    '''
    return re.search(regex, email)
