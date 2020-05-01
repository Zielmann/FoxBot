import os
import csv
import random
import util
import settings
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command

def writeSpeciesToCSV(name, species):
    """
    Stores name/species pair into "Data/tfList.csv"
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

# Gets name/species pair from file. Return 'a human' if user not in list
def readSpeciesFromCSV(name):
    """
    Reads name/species pairs from "Data/tfList.csv"
    Returns the species for the specified name
    The default return value is "a human" if the name is not found
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
    A second message argument after the @ of the user will specify the animal to tf into
    """
    response = ''
    if ctx.author.is_mod and util.validateName(ctx.content):
        # Get name without @
        name = ctx.content.split()[1][1:]
        current_species = new_species = readSpeciesFromCSV(name)
        # Get random species from list
        with open('Data/species.txt') as f:
            all_species = f.read().splitlines()
            while current_species == new_species:
                new_species = random.choice(all_species)
        writeSpeciesToCSV(name, new_species)
        response = name + ' has been TFed into ' + new_species + '!'
    # Check if command sent by streamer and contains name and species
    elif ctx.author.name.lower() == settings.get_channel().lower() and not util.validateNumParameters(ctx.content, 1):
        name = ctx.content.split()[1][1:]
        species = ctx.content.split()[2:]
        species_str = 'a(n) '
        for thing in species:
            species_str = species_str + thing + ' '
        writeSpeciesToCSV(name, species_str)
        response = name + ' has been TFed into ' + species_str[:-1] + '!'
    return response

def tfcheck(ctx):
    """
    Returns the species of the user that calls the command
    """
    # Get name of user that sent the command
    name = ctx.author.name
    species = readSpeciesFromCSV(name)
    return name + ' is ' + species + '!'

def un_tf(ctx):
    """
    Reverts the specified user into a human
    """
    response = ''
    # Mod check
    if ctx.author.is_mod and util.validateName(ctx.content):
        name = ctx.content.split()[1][1:]
        current_species = readSpeciesFromCSV(name)
        # TODO #4: We could probably just delete their name from the CSV
        if current_species == 'a human':
            response = name + ' is already a human'
        else:
            species = 'a human'
            writeSpeciesToCSV(name, species)
            response = name + ' has changed back into ' + species
    return response

def redeem_random(ctx):
    """
    Transforms the caller into a random animal
    """
    response = ''
    name = ctx.tags['display-name']
    current_species = new_species = readSpeciesFromCSV(name)
    # Get random species from list
    with open('Data/species.txt') as f:
        all_species = f.read().splitlines()
        while current_species == new_species:
            new_species = random.choice(all_species)
    writeSpeciesToCSV(name, new_species)
    response = name + ' has been TFed into ' + new_species + '!'
    return response

def redeem_direct(ctx):
    """
    Transforms the caller into the specified animal
    """
    response = ''
    name = ctx.tags['display-name']
    species = 'a(n) ' + str(ctx.content)
    writeSpeciesToCSV(name,species)
    response = name + ' has been TFed into ' + species + '!'
    return response

@cog()
class Tf:

    # Moderator only. TF specified user into a random animal
    @command(name='tf', aliases = ['Tf', 'TF'])
    async def spin_roulette(self, ctx):
        message = tf(ctx)
        await ctx.channel.send(message)

    # Allow user to check their TF status
    @command(name='tfcheck', aliases = ['Tfcheck', 'TFcheck', 'TFCheck'])
    async def check_tf(self, ctx):
        message = tfcheck(ctx)
        await ctx.channel.send(message)

    # Moderator only. Revert specified user back to a human
    @command(name='revert')    
    async def un_TF(self, ctx):
        message = un_tf(ctx)
        await ctx.channel.send(message)
