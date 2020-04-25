import csv
import os
import json
from twitch import TwitchHelix

# Stores name/species pair into file
def writeSpeciesToCSV(name, species):
    lowerName = name.lower()
    userDict = {}
    if os.path.isfile('tfList.csv'):
        with open('tfList.csv', "r") as csv_file:
            reader = csv.reader(csv_file)
            userDict = {rows[0]:rows[1] for rows in reader}
    userDict[lowerName] = species
    with open('tfList.csv', "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for item in userDict:
            writer.writerow([item, userDict[item]])

# Gets name/species pair from file. Return 'a human' if user not in list
def readSpeciesFromCSV(name):
    species = 'a human'
    if os.path.isfile('tflist.csv'):  
        with open('tfList.csv', "r") as csv_file:
            tf_list = csv.DictReader(csv_file, fieldnames=['name', 'species'])
            for entry in tf_list:
                if entry["name"] == name.lower():
                    species = entry["species"]
    return species

# Validates the second parameter starts with @
def validateName(content):
    valid = False
    if validateNumParameters(content, 2):
        if content.split()[1][0] == '@':
            valid = True
    return valid

# Validates the amount of parameters of a ctx context 
def validateNumParameters(content, num):
    splitContent = content.split()
    valid = False
    if len(splitContent) == num:
        valid = True
    return valid    

# Twitch API call to get stream's game ID
def checkGame(ctx, client_id, channel, game_name):
    if getGameName(ctx,client_id,channel).lower() == game_name.lower():
        return True
    else:
        return False

# Twitch API calls to get stream's current game by name
def getGameName(ctx,client_id,channel):
    client = TwitchHelix(client_id)
    stream = client.get_streams(user_logins=channel)._queue[0]
    game_id = stream["game_id"]
    game_info = client.get_games(game_ids=game_id)
    game_name = game_info[0]["name"]
    return game_name
