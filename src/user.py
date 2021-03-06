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
    """ Gets the details of user with u_id

    Parameters:
        u_id (int): User ID
        token (str): The token of the active user

    Returns:
        user (dictionary): A dictionary of all the user's
        details

    """
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
    """ Changes the name of the current user

    Parameters:
        token (str): Token of the current user
        name_first (str): The new first name
        name_last (str): The new last name

    Returns:
        {} : Empty dictionary

    """
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
    """ Changes the email of the current user

    Parameters:
        token (str): Token of the current user
        email (str): The new email

    Returns:
        {} : Empty dictionary

    """
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
    """ Changes the handle of the current user

    Parameters:
        token (str): Token of the current user
        handle_str (str): The new email

    Returns:
        {} : Empty dictionary

    """
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
    """ Changes the profile picture of the current user

    Parameters:
        token (str): Token of the current user
        img_url (str): The URL of the image
        x_start (int): The starting x coordinate
        y_start (int): The starting y coordinate
        x_end (int): The ending x coordinate
        y_end (int): The ending y coordinate

    Returns:
        {} : Empty dictionary

    """
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
    """ Checks to see if an email exists

    Parameters:
        email (str): Email to search for

    Returns:
        bool : True or False depending if the email was
        found

    """
    DATA = getData()
    for users in DATA['users']:
        if users['email'] == email:
            return False
    return True

def user_handle_check(handle):
    """ Checks to see if an handle exists

    Parameters:
        handle (str): Email to search for

    Returns:
        bool : True or False depending if the handle was
        found

    """
    DATA = getData()
    for users in DATA['users']:
        if users['handle_str'] == handle:
            return False
    return True

def user_name_length_check(name):
    """ Checks to see if name is valid

    Parameters:
        name (str): Name to check

    Returns:
        bool : True or False depending if the name was
        valid

    """
    if not name or len(name) > 50:
        return False
    return True

def user_handle_length_check(handle):
    """ Checks to see if handle is valid

    Parameters:
        handle (str): Handle to check

    Returns:
        bool : True or False depending if the handle was
        valid

    """
    if len(handle) < 2 or len(handle) > 20:
        return False
    return True

# Make a regular expression
# for validating an Email
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

# Define a function for
# for validating an Email
def check(email):
    """ Checks to see if email is valid

    Parameters:
        email (str): Email to check

    Returns:
        bool : True or False depending if the email was
        valid

    """
    return re.search(regex, email)
