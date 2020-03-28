'''
This file contains the test methods for the server.py methods
that are associated to the auth file
'''
import urllib
import json
import auth
import server
import database
import pytest
import sys
from error import InputError, AccessError
from urllib.error import HTTPError
from flask import request

BASE_URL = "http://127.0.0.1:8081"

def test_register():
    '''
    This test method will try and create a user using the an email,
    password, and name.  If the output of the flask methods are not null,
    then an id and token were created for the user which indicates a 
    successful registration of the user
    '''
    data = json.dumps({
    	'email': 'paul@gmail.com',
    	'password': '123password',
    	'name_first': 'Paul',
    	'name_last': 'Velliotis'
    	}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register",
                                data=data,
                                headers={'Content-Type': 'application/json'},
                                method='POST')
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    assert (payload['u_id'] is not None) and (payload['token'] is not None)
    
def test_logout():
    '''
    This method will try to logout the user's account after 
    having just registered for one.  The output of the flask method
    will be a dictionary that states whether the operation was 
    successful or not
    '''
    data = json.dumps({
        'email': 'tim@gmail.com',
        'password': '123password',
        'name_first': 'Tim',
        'name_last': 'Smith'
        }).encode('utf-8')
        
    req = urllib.request.Request(f"{BASE_URL}/auth/register",
                                data=data,
                                headers={'Content-Type': 'application/json'},
                                method='POST')

    response = urllib.request.urlopen(req)
    payload = json.load(response)

    user_token = payload['token']

    data = json.dumps({
            'token': user_token
        }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/logout",
                                data=data,
                                headers={'Content-Type': 'application/json'},
                                method='POST')
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    assert payload['is_success'] == True
    
def test_login():

    data = json.dumps({
        'email': 'Oliver@gmail.com',
        'password': '123password',
        'name_first': 'Oliver',
        'name_last': 'Reece'
        }).encode('utf-8')
        
    req = urllib.request.Request(f"{BASE_URL}/auth/register",
                                data=data,
                                headers={'Content-Type': 'application/json'},
                                method='POST')

    response = urllib.request.urlopen(req)
    payload = json.load(response)
    
    user_u_id = payload['u_id']
    user_token = payload['token']

    data = json.dumps({
            'token': user_token
        }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/logout",
                                data=data,
                                headers={'Content-Type': 'application/json'},
                                method='POST')
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    data = json.dumps({
            'email': 'Oliver@gmail.com',
            'password': '123password'
        }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/login",
                                data=data,
                                headers={'Content-Type': 'application/json'},
                                method='POST')
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    assert payload['u_id'] == user_u_id and payload['token'] is not None
