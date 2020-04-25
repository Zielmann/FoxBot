import util
import logging
import botActions
import settings
import importlib
from twitchio.ext import commands

# Load settings from settings.xml
settings.load_settings()

# Set up basic logging handler
if settings.get_logging().lower() == 'debug':
    logLevel = logging.DEBUG
else:
    logLevel = logging.CRITICAL

logging.basicConfig(filename='FoxBot_log.txt', level=logLevel, format='%(asctime)s - %(levelname)s - %(message)s')


# Initialize twitchio command bot
bot = commands.Bot(
    irc_token= settings.get_app_token(),
    client_id= settings.get_client_id(),
    nick= settings.get_bot_account(),
    prefix= settings.get_prefix(),
    initial_channels=[settings.get_channel()]
)

#---------------------------------------------------#

# Bot startup confirmation
@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{settings.get_bot_account()} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(settings.get_channel(), f"/me is alive!")

# Read incoming messages
@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'
    logging.debug('### NEW MESSAGE ###')
    logging.debug(ctx.content)
    logging.debug(ctx.author)
    if 'custom-reward-id' in ctx.tags and ctx.tags['custom-reward-id'] == botActions.get_random_tf_id():
        reply = botActions.redeem_random(ctx)
        await ctx.channel.send(reply)
    elif 'custom-reward-id' in ctx.tags and ctx.tags['custom-reward-id'] == botActions.get_direct_tf_id():
        reply = botActions.redeem_direct(ctx)
        await ctx.channel.send(reply)
    await bot.handle_commands(ctx)


#---------------------#
#---Emote Reactions---#
#---------------------#

@bot.command(name='Oof')
async def oof(ctx):
    message = botActions.oof()
    await ctx.channel.send(message)

@bot.command(name='Heart')
async def heart(ctx):
    message = botActions.heart()
    await ctx.channel.send(message)


#-----------------#
#---TF Commands---#
#-----------------#

# Moderator only. TF specified user into a random animal
@bot.command(name='tf', aliases = ['Tf', 'TF'])
async def spin_roulette(ctx):
    message = botActions.tf(ctx)
    await ctx.channel.send(message)

# Allow user to check their TF status
@bot.command(name='tfcheck', aliases = ['Tfcheck', 'TFcheck', 'TFCheck'])
async def get_species(ctx):
    message = botActions.tfcheck(ctx)
    await ctx.channel.send(message)

# Moderator only. Revert specified user back to a human
@bot.command(name='revert')    
async def un_TF(ctx):
    message = botActions.un_tf(ctx)
    await ctx.channel.send(message)

#----------------------------#
#---Game-Specific Commands---#
#----------------------------#

# List mods for active game based on info provided in settings.xml
# Currently only support Rimworld and Factorio
@bot.command(name='mods', aliases = ['Mods'])
async def get_mods(ctx):
    message = botActions.get_mods(ctx)
    await ctx.channel.send(message)

# Send valid rimworld commands if rimworld is being played
@bot.command(name='rimworld', aliases = ['Rimworld'])
async def rimworld_commands(ctx):
    message = botActions.rimworld_commands(ctx)
    await ctx.channel.send(message)

# Rimworld item lookup. Responds with all matching items and their cost, 500ch response max.
@bot.command(name='item', aliases=['items', 'Item', 'Items'])
async def item_lookup(ctx):
    message = botActions.item_lookup(ctx, logging)
    await ctx.channel.send(message)

# Rimworld event lookup. Responds with all matching events and their cost, 500ch response max.
@bot.command(name='event', aliases=['events', 'Event', 'Events'])
async def event_lookup(ctx):
    message = botActions.event_lookup(ctx)
    await ctx.channel.send(message)

# Lookup detailed info for a specific event. Search term must be an exact match
@bot.command(name='eventinfo', aliases = ['Eventinfo','EventInfo'])
async def event_details(ctx):
    message = botActions.event_details(ctx)
    await ctx.channel.send(message)

# Lookup detailed info for a specific item. Search term must be an exact match        
@bot.command(name='iteminfo', aliases = ['Iteminfo','ItemInfo'])        
async def item_details(ctx):
    message = botActions.item_details(ctx, logging)
    await ctx.channel.send(message)

@bot.command(name='avorion', aliases = ['Avorion','ships','Ships'])
async def link_avorion_profile(ctx):
    message = botActions.link_avorion_profile()
    await ctx.channel.send(message)

#--------------------#
#---Empty Commands---#
#--------------------#
# This section is set up to reduce "unrecognized command" output to the console.

# Do nothing in case first word of a message is 'haurbus'
@bot.command(name='s')
async def do_nothing(ctx):
    await ctx.channel.send('')

# Do nothing in response to the TwitchToolkit commands in rimworld

@bot.command(name='bal', aliases=['balance', 'coins', 'buy', 'lookup', 'joinqueue', 'mypawnhealth', 'mypawnbody', 'purchaselist', 'modsettings', 'giftcoins', 'mypawnstory'])
async def nothing(ctx):
    await ctx.channel.send('')

#----------------------------------------------------#

if __name__ == "__main__":
    bot.load_module('Modules.basics')
    bot.load_module('Modules.raffle')
    bot.load_module('Modules.quotes')
    bot.run()   
