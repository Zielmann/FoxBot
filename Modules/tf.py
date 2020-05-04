import os
import csv
import random
import util
import settings
import json
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command


def load_tf_list():
    """
    Loads a dictionary of species by username from "Data/tfList.json"

    Returns:
        dict: Contains species by username
    """
    tf = {}
    if os.path.isfile('Data/tfList.json') and os.path.getsize('Data/tfList.json') != 0:
        with open('Data/tfList.json', 'r') as json_file:
            tf = json.load(json_file)
    # TODO: Delete this once Haurbus' list is converted
    # Legacy for converting csv to json method
    elif os.path.isfile('Data/tfList.csv') and os.path.getsize('Data/tfList.csv') != 0:
        with open('Data/tfList.csv', "r") as csv_file:
            tf_list = csv.DictReader(csv_file, fieldnames=['name', 'species'])
            for entry in tf_list:
                tf[entry['name']] = entry['species']
        with open('Data/tfList.json', 'w') as json_file:
            json.dump(tf, json_file, indent=4)
    return tf

tfList = load_tf_list()

def writeSpeciesToJSON(name, species):
    """
    Stores name/species pair into "Data/tfList.json"

    Parameters:
        name (str): The name of user (without the @) to be tfed
        species (str): The species to tf the user into
    """
    tfList[name.lower()] = species
    with open('Data/tfList.json', 'w') as json_file:
        json.dump(tfList, json_file, indent=4)
    return

def writeSpeciesToCSV(name, species):
    """
    DEPRECIATED
    Stores name/species pair into "Data/tfList.csv"

    Parameters:
        name: A string containing the name of user (without the @) to be tfed
        species: A string containing the species to tf the user into
    """
    lowerName = name.lower()
    userDict = {}
    if os.path.isfile('Data/tfList.csv'):
        with open('Data/tfList.csv', "r") as csv_file:
            reader = csv.reader(csv_file)
            userDict = {rows[0]:rows[1] for rows in reader}
    userDict[lowerName] = species
    with open('Data/tfList.csv', "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for item in userDict:
            writer.writerow([item, userDict[item]])

def getSpecies(name):
    """
    Returns the user's current species
    
    Parameters:
        name (str): A string containing the name of user (without the @) to check

    Returns:
        str: The species of the user, 
             the default return value is "a human" if the name is not found
    """
    species = 'a human'
    if name.lower() in tfList:
        species = tfList[name.lower()]
    return species
        
def readSpeciesFromCSV(name):
    """
    DEPRECIATED
    Reads name/species pairs from "Data/tfList.csv"
    
    Parameters:
        name: A string containing the name of user (without the @) to check

    Returns:
        str: the species for the specified name,
             the default return value is "a human" if the name is not found
    """
    species = 'a human'
    if os.path.isfile('Data/tflist.csv'):  
        with open('Data/tfList.csv', "r") as csv_file:
            tf_list = csv.DictReader(csv_file, fieldnames=['name', 'species'])
            for entry in tf_list:
                if entry["name"] == name.lower():
                    species = entry["species"]
                    break
    return species

def tf(ctx):
    """
    TFs the specified user into either a random or specified animal
    
    Parameters:
        ctx - The context of the message, a second message argument after the 
              @ of the user will specify the animal to tf into

    Returns:
        str: A confirmation of the species the user has been tfed into
    """
    response = ''
    if ctx.author.is_mod and util.validateName(ctx.content):
        # Get name without @
        name = ctx.content.split()[1][1:]
        current_species = new_species = getSpecies(name)
        # Get random species from list
        with open('Data/species.txt') as f:
            all_species = f.read().splitlines()
            while current_species == new_species:
                new_species = random.choice(all_species)
        writeSpeciesToJSON(name, new_species)
        response = name + ' has been TFed into ' + new_species + '!'
    # Check if command sent by streamer and contains name and species
    elif ctx.author.name.lower() == settings.get_channel().lower() and not util.validateNumParameters(ctx.content, 1):
        name = ctx.content.split()[1][1:]
        species = ctx.content.split()[2:]
        species_str = 'a(n) '
        for thing in species:
            species_str = species_str + thing + ' '
        writeSpeciesToJSON(name, species_str)
        response = name + ' has been TFed into ' + species_str[:-1] + '!'
    return response

def tfcheck(ctx):
    """
    Returns the species of the message author that calls the command

    Parameters:
        ctx: The context of the message

    Returns:
        str: The species of the user
    """
    # Get name of user that sent the command
    name = ctx.author.name
    species = getSpecies(name)
    return name + ' is ' + species + '!'

def un_tf(ctx):
    """
    Reverts the specified user into a human

    Parameters:
        ctx: The context of the message

    Returns:
        str: Confirmation of the action
    """
    response = ''
    # Mod check
    if ctx.author.is_mod and util.validateName(ctx.content):
        name = ctx.content.split()[1][1:]
        if name.lower() in tfList:
            tfList.pop(name.lower())
            response = name + ' has changed back into a human'
            with open('Data/tfList.json', 'w') as json_file:
                json.dump(tfList, json_file, indent=4)
        else:
            response = name + ' is already a human'

    return response

def redeem_random(ctx):
    """
    Transforms the message author into a random animal

    Parameters:
        ctx: The context of the message

    Returns:
        str: A confirmation of the species the user has been tfed into
    """
    response = ''
    name = ctx.tags['display-name']
    current_species = new_species = getSpecies(name)
    # Get random species from list
    with open('Data/species.txt') as f:
        all_species = f.read().splitlines()
        while current_species == new_species:
            new_species = random.choice(all_species)
    writeSpeciesToJSON(name, new_species)
    response = name + ' has been TFed into ' + new_species + '!'
    return response

def redeem_direct(ctx):
    """
    Transforms the message author into the specified animal

    Parameters:
        ctx: The context of the message

    Returns:
        str: A confirmation of the species the user has been tfed into
    """
    response = ''
    name = ctx.tags['display-name']
    species = 'a(n) ' + str(ctx.content)
    writeSpeciesToJSON(name,species)
    response = name + ' has been TFed into ' + species + '!'
    return response

@cog()
class Tf:

    # Moderator only. TF specified user into a random animal
    @command(name='tf', aliases = ['Tf', 'TF'])
    async def spin_roulette(self, ctx):
        message = tf(ctx)
        if message:
            await ctx.channel.send(message)

    # Allow user to check their TF status
    @command(name='tfcheck', aliases = ['Tfcheck', 'TFcheck', 'TFCheck'])
    async def check_tf(self, ctx):
        message = tfcheck(ctx)
        if message:
            await ctx.channel.send(message)

    # Moderator only. Revert specified user back to a human
    @command(name='revert')    
    async def un_TF(self, ctx):
        message = un_tf(ctx)
        if message:
            await ctx.channel.send(message)

