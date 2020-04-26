import json
import random
import csv
import util
import xmltodict
import logging
import sys
from datetime import datetime
from twitch import TwitchHelix

settings = {}

# settings.xml parser
def load_settings():
    global settings
    with open('settings.xml') as f:
        settings = xmltodict.parse(f.read())['settings']

#--------------------------------------#
# Getters

def get_app_token():
    return settings['bot_setup']['app_token']

def get_client_id():
    return settings['bot_setup']['client_id']

def get_bot_account():
    return settings['bot_setup']['bot_account']

def get_prefix():
    return settings['bot_setup']['command_prefix']

def get_channel():
    return settings['bot_setup']['channel']

def get_logging():
    return settings['bot_setup']['logging']

def get_twitter():
    return settings['social']['twitter']

def get_discord():
    return settings['social']['discord']

def get_rimworld_mods():
    return settings['games']['rimworld']['mods']

def get_rimworld_events():
    return settings['games']['rimworld']['event_file']

def get_rimworld_items():
    return settings['games']['rimworld']['item_file']

def get_factorio_mods():
    return settings['games']['factorio']['mods']

def get_avorion_link():
    return settings['games']['avorion']['profile_link']

def get_random_tf_id():
    return settings['custom_rewards']['random_tf']

def get_direct_tf_id():
    return settings['custom_rewards']['direct_tf']


#---------------------------------------------#
# TF Command Functions

def tf(ctx):
    response = ''
    if ctx.author.is_mod and util.validateName(ctx.content):
        # Get name without @
        name = ctx.content.split()[1][1:]
        current_species = new_species = util.readSpeciesFromCSV(name)
        # Get random species from list
        with open('species.txt') as f:
            all_species = f.read().splitlines()
            while current_species == new_species:
                new_species = random.choice(all_species)
        util.writeSpeciesToCSV(name, new_species)
        response = name + ' has been TFed into ' + new_species + '!'
    # Check if command sent by streamer and contains name and species
    elif ctx.author.name.lower() == get_channel().lower() and not util.validateNumParameters(ctx.content, 1):
        name = ctx.content.split()[1][1:]
        species = ctx.content.split()[2:]
        species_str = 'a(n) '
        for thing in species:
            species_str = species_str + thing + ' '
        util.writeSpeciesToCSV(name, species_str)
        response = name + ' has been TFed into ' + species_str[:-1] + '!'
    return response

def tfcheck(ctx):
    # Get name of user that sent the command
    name = ctx.author.name
    species = util.readSpeciesFromCSV(name)
    return name + ' is ' + species + '!'

def un_tf(ctx):
    response = ''
    # Mod check
    if ctx.author.is_mod and util.validateName(ctx.content):
        name = ctx.content.split()[1][1:]
        current_species = util.readSpeciesFromCSV(name)
        if current_species == 'a human':
            response = name + ' is already a human'
        else:
            species = 'a human'
            util.writeSpeciesToCSV(name, species)
            response = name + ' has changed back into ' + species
    return response

def redeem_random(ctx):
    response = ''
    name = ctx.tags['display-name']
    current_species = new_species = util.readSpeciesFromCSV(name)
    # Get random species from list
    with open('species.txt') as f:
        all_species = f.read().splitlines()
        while current_species == new_species:
            new_species = random.choice(all_species)
    util.writeSpeciesToCSV(name, new_species)
    response = name + ' has been TFed into ' + new_species + '!'
    return response

def redeem_direct(ctx):
    response = ''
    name = ctx.tags['display-name']
    species = 'a(n) ' + str(ctx.content)
    util.writeSpeciesToCSV(name,species)
    response = name + ' has been TFed into ' + species + '!'
    return response

#-----------------------------------------------#
# Game-Specific Functions

def get_mods(ctx):
    response = ''
    if util.checkGame(ctx, get_client_id(), get_channel(),'rimworld'):
        response = get_rimworld_mods()
    elif util.checkGame(ctx, get_client_id(), get_channel(),'factorio'):
        response = get_factorio_mods()
    return response

def rimworld_commands(ctx):
    response = ''
    if util.checkGame(ctx, get_client_id(), get_channel(),'rimworld'):
        response = 'Rimworld Commands: !item, !event, !mods'
    return response

def item_lookup(ctx, logging):
    response = ''
    logging.critical('Item lookup called')
    # Check if current game is Rimworld. Only responds while playing Rimworld
    if util.checkGame(ctx, get_client_id(), get_channel(), 'rimworld') and util.validateNumParameters(ctx.content, 2):
        # Get item to search from message
        search = ctx.content.split()[1].lower()
        logging.critical('Searching for ' + search)
        tries = 2
        # Allows for a retry if the items file had to have the extraneous comma removed to fix the json formatting
        for i in range(tries):
            try:
                with open(get_rimworld_items()) as f:
                    items_json = json.load(f)
                logging.critical('Loaded item list with ' + str(len(items_json["items"])) + ' items')
                break
            except Exception as e:
                logging.critical('Could not load items file at ' + get_rimworld_items())
                logging.critical(str(e))
                comma = destroy_the_comma(logging) # Kill it.
                if not comma:
                    logging.critical("Removed comma from file")
                else:
                    logging.critical("Could not remove comma from file")

        # Find all items containing search term and append to response string
        for field in items_json["items"]:
            if search in field["abr"]:
                response = response + field["abr"] + ':' + str(field["price"]) + ', '
                logging.critical('Found match: ' + field["abr"])

        # Trim response below 500ch max if necessary
        if len(response) > 500:
            response = response[0:495]+ ' ...  '
        # Cut trailing ', ' from response
        response = response[:-2]
    logging.debug('Response: ' + response)
    return response

def event_lookup(ctx):
    response = ''
        # Only respond if current game is Rimworld
    if util.checkGame(ctx, get_client_id(), get_channel(), 'rimworld') and util.validateNumParameters(ctx.content, 2):
        search = ctx.content.split()[1].lower()
        with open(get_rimworld_events()) as e:
            events = json.load(e)

        # Follows same logic as item search
        for field in events["incitems"]:
            if search in field["abr"]:
                response = response + field["abr"] + ':' + str(field["price"]) + ', '
        if len(response) > 500:
            response = response[0:495]+ ' ...  '
        response = response[:-2]
    return response

def event_details(ctx):
    response = ''
    if util.checkGame(ctx, get_client_id(), get_channel(),'rimworld') and util.validateNumParameters(ctx.content, 2):
        search = ctx.content.split()[1].lower()
        with open(get_rimworld_events()) as e:
            events = json.load(e)
        for entry in events["incitems"]:
            if entry["abr"] == search:
                response = 'Event ' + search + ' costs ' + str(entry["price"]) + ' coins. Karma type: ' + entry["karmatype"]
    return response

def item_details(ctx,logging):
    response = ''
    if util.checkGame(ctx, get_client_id(), get_channel(),'rimworld') and util.validateNumParameters(ctx.content, 2):
        search = ctx.content.split()[1].lower()
        tries = 2
        for i in range(tries):
            try:
                with open(get_rimworld_items()) as i:
                    items = json.load(i)
                logging.critical('Loaded item list with ' + str(len(items["items"])) + ' items')
                break
            except Exception as e:
                logging.critical('Could not load items file at ' + get_rimworld_items())
                logging.critical(str(e))
                comma = destroy_the_comma(logging)
                if not comma:
                    logging.critical("Removed comma from file")
                else:
                    logging.critical("Could not remove comma from file")

        for entry in items["items"]:
            if entry["abr"] == search:
                response = 'Item ' + search + ' costs ' + str(entry["price"]) + ' coins. Item category: ' + entry["category"]
    return response

# Deletes extraneous comma in StoreItems.json file if it exists
def destroy_the_comma(logging):
    comma = True
    fix = False
    logging.critical("Trying to fix StoreItems.json")
    try:
        with open(get_rimworld_items(), 'r') as f:
            raw_data = f.read().splitlines()
        # StoreItems.json file sometimes gets corrupted by an extra comma after the } four lines from the end of the file
        # Check to make sure the comma is the issue. If so, remove the comma
        if(raw_data[-4] == '\t},'):
            raw_data[-4] = '\t}'
            fix = True
        if fix:
            with open(get_rimworld_items(),'w') as f:
                f.writelines(line + '\n' for line in raw_data)
            comma = False
    except Exception as e:
        logging.critical(str(e))
    return comma

def link_avorion_profile():
    response = 'Haurbus makes ships! Check them out here: ' + get_avorion_link()
    return response
