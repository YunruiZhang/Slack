'''
This file contains information about anything relating to all the other
functions.  The methods in this file relate to listing all users, searching,
and hangman.  There are some helper methods that just check the
existence of channels and users and the game state of hangman.
'''
import urllib.request
from random import randint
from database import *
from channel import *
from error import *
from auth import *
from message import *

def users_all(token):
    """ Gets all the users in Slackr

    Parameters:
        token(str): Token of the active user

    Returns:
       users (dictionary): List of dictionaries, where each dictionary contains
       types u_id, email, name_first, name_last, handle_str, profile_img_url
    """
    all_user = []
    Data = getData()

    operate_u_id = verify_token(token)
    if not operate_u_id:
        raise AccessError('Token Invalid')
    for user in Data['users']:
        to_add = {
            'u_id': user['u_id'],
            'name_first': user['name_first'],
            'name_last':user['name_last'],
            #'permission_id': user['permission_id'],
            'email': user['email'],
            'handle_str': user['handle_str'],
            'profile_img_url': user['profile_img_url']
        }
        all_user.append(to_add)

    return {"users":all_user}

def search(token, query_str):
    """ Searches all the messages in Slackr

    Parameters:
        token(str): Token of the active user
        query_str(str): Query to search

    Returns:
       messages (dictionary): List of dictionaries, where each dictionary contains types
       { message_id, u_id, message, time_created, reacts, is_pinned  }
    """

    if not verify_token(token):
        raise AccessError('Invalid Token')

    search_message = []
    Data = getData()

    for channels in Data['channels']:
        curr_list = channels['messages']
        for i in curr_list:
            if query_str in i['message']:
                search_message.append(i)

    newlist = sorted(search_message, key=lambda k: k['time_created'])

    return {'messages' : newlist}

def hangman_start(token, channel_id):
    """ Start a game of hangman

    Parameters:
        token(str): Token of the active user
        channel_id(int): ID of the channel

    Returns:
       None
    """
    DATA = getData()

    bot_id = None
    bot_token = None

    word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    response = urllib.request.urlopen(word_url)
    long_txt = response.read().decode()
    words = long_txt.splitlines()

    if not verify_token(token):
        raise AccessError("Not valid user")

    found_flag = False
    for users in DATA["users"]:
        if users['email'] == "hangmanbot@t18a-welv.com":
            found_flag = True
            bot_id = users['u_id']
            bot_token = users['token']
            break

    if not found_flag:
        bot_details = auth_register("hangmanbot@t18a-welv.com", "hangman123", "Hangman", "Bot")
        bot_id = bot_details['u_id']
        bot_token = bot_details['token']
        DATA = getData()

    for channel in DATA["channels"]:
        if channel["channel_id"] == int(channel_id):
            already_in_channel = False
            for user in channel['details']['all_members']:
                if user['u_id'] == bot_id:
                    already_in_channel = True
            if not already_in_channel:
                user_to_add = {
                    'u_id':bot_id,
                    'name_first': 'Hangman',
                    'name_last': 'Bot'
                }

                channel['details']['all_members'].append(user_to_add)
            break
    update_database(DATA)

    #print(words)
    word_to_guess = words[randint(0, len(words))].upper()
    word_string = ""
    for character in word_to_guess:
        if character != "":
            word_string += "_"
        else:
            word_string += "    "
    print(word_string)
    print(word_to_guess)
    print(bot_token)

    for channel in DATA["channels"]:
        if channel["channel_id"] == int(channel_id):
            channel["hangman"]["is_active"] = True
            channel["hangman"]["word_to_guess"] = word_to_guess
            channel["hangman"]["guess_string"] = list(word_string)
            break
    update_database(DATA)
    message_send(bot_token, channel_id, "Welcome to Hangman!\n\nWord: "+" ".join(word_string))
    return {}

def hangman_guess(token, channel_id, character):
    """ Make a guess for a game of hangman

    Parameters:
        token(str): Token of the active user
        channel_id(int): ID of the channel
        character(char): Character to guess

    Returns:
       None
    """
    DATA = getData()
    character = character.upper()
    found_flag = False

    for channel in DATA["channels"]:
        if channel["channel_id"] == int(channel_id):
            if channel["hangman"]["is_active"]:
                found_flag = True
                break

    if not found_flag:
        raise InputError("No active hangman game")

    if not verify_token(token):
        raise AccessError("Not valid user")

    bot_token = None
    for users in DATA["users"]:
        if users['email'] == "hangmanbot@t18a-welv.com":
            found_flag = True
            bot_id = users['u_id']
            bot_token = users['token']
            break

    word_to_guess = channel["hangman"]["word_to_guess"]
    guess_string = channel["hangman"]["guess_string"]

    #print(word_to_guess)
    #print(character)
    #print(character in word_to_guess)

    #Wrong Guess
    if character not in word_to_guess:
        channel["hangman"]["guess_list"].append(character)
        guessed_string = []
        for characters in channel["hangman"]["guess_list"]:
            guessed_string.append(characters+" ")
        update_database(DATA)
        DATA = getData
        #Killed the guy
        if len(channel["hangman"]["guess_list"]) == 9:
            message_send(bot_token, channel_id, word_to_guess + "\nYou lost!\n" + hangman_ascii(len(channel["hangman"]["guess_list"])) + "\nYou have guessed: " + "".join(guessed_string))
            channel["hangman"]["is_active"] = False
            channel["hangman"]["word_to_guess"] = None
            channel["hangman"]["guess_string"] = None
            channel["hangman"]["guess_lists"] = None
            DATA = getData()
            #update_database(DATA)
        else:
            print(bot_token)
            print(guess_string)

            message_send(bot_token, channel_id, ""+" ".join(guess_string)+"\n"+hangman_ascii(len(channel["hangman"]["guess_list"]))+"\nYou have guessed: "+"".join(guessed_string))
            DATA = getData()
            #update_database(DATA)

    else:
        guessed_string = []
        for characters in channel["hangman"]["guess_list"]:
            guessed_string.append(characters)
        for index in range(0, len(word_to_guess)):
            if list(word_to_guess)[index] == character:
                guess_string[index] = character

        update_database(DATA)
        DATA = getData()

        #print("".join(guessed_string))
        #print(word_to_guess)

        if "_" not in guess_string:
            message_send(bot_token, channel_id, word_to_guess+"\nCongratulations! You have won hangman.")
            channel["hangman"]["is_active"] = False
            channel["hangman"]["word_to_guess"] = None
            channel["hangman"]["guess_string"] = None
            channel["hangman"]["guess_list"] = None

            DATA = getData()
            #update_database(DATA)
        else:
            #print(str(guess_string)+"\n"+str(hangman_ascii(len(channel["hangman"]["guess_list"])))+"\nYou have guessed: "+str(guessed_string))
            channel["hangman"]["guess_string"] = guess_string
            update_database(DATA)
            #print(" ".join(guess_string)+"\n"+hangman_ascii(len(channel["hangman"]["guess_list"]))+"\nYou have guessed: ".join(guessed_string))
            message_send(bot_token, channel_id, ""+" ".join(guess_string)+"\n"+hangman_ascii(len(channel["hangman"]["guess_list"]))+"\nYou have guessed: "+"".join(guessed_string))
            DATA = getData()
            #update_database(DATA)
    update_database(DATA)
    return {}

def hangman_ascii(wrong_guesses):
    """ ASCII designs for hangman state

    Parameters:
        wrong_guesses(int): The number of wrong guesses

    Returns:
       string (str): String of the game state as ASCII art
    """
    if (wrong_guesses) == 1:
        return "    ========="
    elif (wrong_guesses) == 2:
        return "    |\n    |\n    |\n    |\n    ========="
    elif (wrong_guesses) == 3:
        return "    +----------\n    |\n    |\n    |\n    |\n    ========="
    elif (wrong_guesses) == 4:
        return "    +----------\n    |       |\n    |\n    |\n    |\n    ========="
    elif (wrong_guesses) == 5:
        return "    +----------\n    |       |\n    |       O\n    |\n    |\n    ========="
    elif (wrong_guesses) == 6:
        return "    +----------\n    |       |\n    |       O\n    |      /|\n    |\n    ========="
    elif (wrong_guesses) == 7:
        return "    +----------\n    |       |\n    |       O\n    |      /|\\ \n    |\n    ========="
    elif (wrong_guesses) == 8:
        return "    +----------\n    |       |\n    |       O\n    |      /|\\ \n    |      /\n    ========="
    elif (wrong_guesses) == 9:
        return "    +----------\n    |       |\n    |       O\n    |      /|\\ \n    |      /\\ \n    ========="

    return ""
