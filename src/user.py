import re
from database import *
from channel import *
from error import *
from PIL import Image
import urllib
import io
from io import StringIO
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import imghdr
import pathlib

def user_profile(token, u_id):

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
        'handle_str' : users['handle_str']
    }
    update_database(DATA)
    return return_user

def user_profile_setname(token, name_first, name_last):
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
    DATA = getData()
    fd = urllib.request.urlopen(img_url)
    image_file = io.BytesIO(fd.read())

    if not fd:
        raise InputError("Image URL invalid")

    if imghdr.what(image_file) != "jpeg":
        raise InputError("Not a JPG file")

    img = Image.open(image_file)
    width, height = img.size

    if x_start < 0 or y_start < 0:
        raise InputError("Coordinates not within the bounds of the image")

    if x_end-x_start > width or y_end - y_start > height:
        raise InputError("Coordinates not within the bounds of the image")      

    cropped_image = img.crop((x_start, y_start, x_end, y_end))
    u_id = verify_token(token)

    UPLOAD_FOLDER = './profile_photos'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    filename = secure_filename(cropped_image.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #cropped_image.save(pathlib.Path(str(pathlib.Path().absolute())+"/profile_photos/profile_id"+u_id+".jpg"))
    #cropped_image.show()

    for users in DATA['users']:
        if users["u_id"] == int(u_id):
            users["profile_img_url"] = str(url_for('uploaded_file',filename=filename))
            break

    update_database(DATA)
    return {}


def user_email_check(email): 
    DATA = getData()
    for users in DATA['users']:
        if users['email'] == email:
            return False
    return True

def user_handle_check(handle):
    DATA = getData()
    for users in DATA['users']:
        if users['handle_str'] == handle:
            return False
    return True

def user_name_length_check(name):
    if not name or len(name) > 50:
        return False
    return True

def user_handle_length_check(handle):
    if len(handle) < 2 or len(handle) > 20:
        return False
    return True

# Make a regular expression
# for validating an Email
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

# Define a function for
# for validating an Email
def check(email):
    return re.search(regex, email)
