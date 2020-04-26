import util
import settings
import json
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command

def commands(ctx):
    response = ''
    if util.checkGame(ctx, settings.get_client_id(), settings.get_channel(),'rimworld'):
        response = 'Rimworld Commands: !item, !event, !iteminfo, !eventinfo, !mods'
    return response

def item_search(ctx):
    response = ''
    # Check if current game is Rimworld. Only responds while playing Rimworld
    if util.checkGame(ctx, settings.get_client_id(), settings.get_channel(), 'rimworld') and util.validateNumParameters(ctx.content, 2):
        # Get item to search from message
        search = ctx.content.split()[1].lower()
        tries = 2
        # Allows for a retry if the items file had to have the extraneous comma removed to fix the json formatting
        for i in range(tries):
            try:
                with open(settings.get_rimworld_items()) as f:
                    items_json = json.load(f)
                break
            except Exception as e:
                print(e)
                destroy_the_comma() # Kill it.

        # Find all items containing search term and append to response string
        for field in items_json["items"]:
            if search in field["abr"]:
                response = response + field["abr"] + ':' + str(field["price"]) + ', '

        # Trim response below 500ch max if necessary
        if len(response) > 500:
            response = response[0:495]+ ' ...  '
        # Cut trailing ', ' from response
        response = response[:-2]
    return response

def event_search(ctx):
    response = ''
        # Only respond if current game is Rimworld
    if util.checkGame(ctx, settings.get_client_id(), settings.get_channel(), 'rimworld') and util.validateNumParameters(ctx.content, 2):
        search = ctx.content.split()[1].lower()
        with open(settings.get_rimworld_events()) as e:
            events = json.load(e)

        # Follows same logic as item search
        for field in events["incitems"]:
            if search in field["abr"]:
                response = response + field["abr"] + ':' + str(field["price"]) + ', '
        if len(response) > 500:
            response = response[0:495]+ ' ...  '
        response = response[:-2]
    return response

def event_detail_search(ctx):
    response = ''
    if util.checkGame(ctx, settings.get_client_id(), settings.get_channel(),'rimworld') and util.validateNumParameters(ctx.content, 2):
        search = ctx.content.split()[1].lower()
        with open(settings.get_rimworld_events()) as e:
            events = json.load(e)
        for entry in events["incitems"]:
            if entry["abr"] == search:
                response = 'Event ' + search + ' costs ' + str(entry["price"]) + ' coins. Karma type: ' + entry["karmatype"]
    return response

def item_detail_search(ctx):
    response = ''
    if util.checkGame(ctx, settings.get_client_id(), settings.get_channel(),'rimworld') and util.validateNumParameters(ctx.content, 2):
        search = ctx.content.split()[1].lower()
        tries = 2
        for i in range(tries):
            try:
                with open(settings.get_rimworld_items()) as i:
                    items = json.load(i)
                break
            except Exception as e:
                print(e)
                destroy_the_comma()

        for entry in items["items"]:
            if entry["abr"] == search:
                response = 'Item ' + search + ' costs ' + str(entry["price"]) + ' coins. Item category: ' + entry["category"]
    return response

# Deletes extraneous comma in StoreItems.json file if it exists
def destroy_the_comma():
    comma = True
    fix = False
    try:
        with open(settings.get_rimworld_items(), 'r') as f:
            raw_data = f.read().splitlines()
        # StoreItems.json file sometimes gets corrupted by an extra comma after the } four lines from the end of the file
        # Check to make sure the comma is the issue. If so, remove the comma
        if(raw_data[-4] == '\t},'):
            raw_data[-4] = '\t}'
            fix = True
        if fix:
            with open(settings.get_rimworld_items(),'w') as f:
                f.writelines(line + '\n' for line in raw_data)
            comma = False
    except Exception as e:
        print(e)
    return comma

@cog()
class Rimworld:
    # Send valid rimworld commands if rimworld is being played
    @command(name='rimworld', aliases = ['Rimworld'])
    async def rimworld_commands(self, ctx):
        message = commands(ctx)
        await ctx.channel.send(message)

    # Rimworld item lookup. Responds with all matching items and their cost, 500ch response max.
    @command(name='item', aliases=['items', 'Item', 'Items'])
    async def item_lookup(self, ctx):
        message = item_search(ctx)
        await ctx.channel.send(message)

    # Rimworld event lookup. Responds with all matching events and their cost, 500ch response max.
    @command(name='event', aliases=['events', 'Event', 'Events'])
    async def event_lookup(self, ctx):
        message = event_search(ctx)
        await ctx.channel.send(message)

    # Lookup detailed info for a specific event. Search term must be an exact match
    @command(name='eventinfo', aliases = ['Eventinfo','EventInfo'])
    async def event_details(self, ctx):
        message = event_detail_search(ctx)
        await ctx.channel.send(message)

    # Lookup detailed info for a specific item. Search term must be an exact match        
    @command(name='iteminfo', aliases = ['Iteminfo','ItemInfo'])        
    async def item_details(self, ctx):
        message = item_detail_search(ctx)
        await ctx.channel.send(message)

    # Used to prevent nuisance output to the terminal when running alongside the Rimworld TwitchToolkit bot
    @command(name='bal', aliases=['balance', 'coins', 'buy', 'lookup', 'joinqueue', 'mypawnhealth', 'mypawnbody', 'purchaselist', 'modsettings', 'giftcoins', 'mypawnstory'])
    async def nothing(self, ctx):
        await ctx.channel.send('')
