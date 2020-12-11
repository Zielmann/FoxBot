import random
import util
import settings
from datetime import datetime
from twitch import TwitchHelix
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command

def get_bot_info():
    """
    Returns a string of information about FoxBot

    Returns:
        str: Contains the authors and notes about the bot. 
    """
    return 'FoxBot is written in Python by @zielfoxx and @YorkRacc. !commands for available commands. Ideas/Feedback always welcome!'

def get_github():
    """
    Returns a string containing the repository for FoxBot

    Returns:
        str: Contains the link to the Github repository for FoxBot
    """
    return 'Link to FoxBot repository: https://github.com/Zielmann/Foxbot'
    
def get_commands():
    """
    Returns a string of all available twitch chat commands

    Returns:
        str: Contains all of the available commands to call
    """
    return 'Available Commands: !bot, !github, !discord, !twitter, !avorion, !tfcheck, !quote'

def get_uptime():
    """
    Returns a string of the current uptime

    Returns:
        str: Contains the current amount of uptime for the channel
    """
    # Set up twitch API call and get stream info
    client = TwitchHelix(client_id = settings.get_client_id())
    stream = client.get_streams(user_logins = settings.get_channel())._queue[0]
    # Get stream start time (API sends UTC time) and calculate uptime
    start_time = stream["started_at"]
    uptime = datetime.utcnow() - start_time
    return str(uptime).split(".")[0]

def get_shoutout(ctx):
    """
    Returns a string with the twitch.tv link for the said user

    Returns:
        str: Contains the twitch.tv link for the said user.
    """
    response = ''
    if util.validateName(ctx.content):
        name = ctx.content.split()[1][1:]
        response = 'Shoutout to ' + name + '! Check out their stream at twitch.tv/' + name + ' and give them a follow!'
    return response

def get_twitter():
    """
    Returns a string containing the Twitter link for the streamer

    Returns:
        str: Contains Twitter link indicated in settings file
    """
    response = ''
    if settings.get_twitter():
        response = settings.get_twitter()
    return response

def get_discord():
    """
    Returns a string containing the discord link for the streamer

    Returns:
        str: Contains Discord link indicated in settings file
    """
    response = ''
    if settings.get_discord():
        response = settings.get_discord()
    return response

# def get_mods(ctx): NOT CURRENTLY SUPPORTED - API calls not working
#     """
#     Returns a string containing the mods for the current game being played

#     Parameters:
#         ctx - The context of the message

#     Returns:
#         str: Contains a list of mods for the game listed by twitch
#     """
#     response = ''
#     if util.checkGame(ctx, settings.get_client_id(), settings.get_channel(),'rimworld'):
#         response = settings.get_rimworld_mods()
#     elif util.checkGame(ctx, settings.get_client_id(), settings.get_channel(),'factorio'):
#         response = settings.get_factorio_mods()
#     return response

def link_avorion():
    """
    Returns a string containing the link for an avorion steam workshop page

    Returns:
        str: Contains the steam workshop link indicated by the settings file
    """
    response = ''
    if settings.avorion_enabled():
        response = settings.get_avorion_link()
    return response

@cog()
class Basics:

    # Post general info about the bot
    @command(name='bot', aliases=['info', 'Bot', 'Info'])
    async def bot_info(self, ctx):
        message = get_bot_info()
        if message:
            await ctx.channel.send(message)

    # Link the github repository
    @command(name='github', aliases=['Github', 'repo', 'Repo'])
    async def github(self, ctx):
        message = get_github()
        if message:
            await ctx.channel.send(message)

    # List all general commands
    @command(name='commands', aliases=['help', 'Commands', 'Help'])
    async def list_commands(self, ctx):
        message = get_commands()
        if message:
            await ctx.channel.send(message)

    # Get stream uptime. Responds with stream uptime
    @command(name='uptime', aliases = ['Uptime'])
    async def uptime(self, ctx):
        message = get_uptime()
        if message:
            await ctx.channel.send(message)

    # Send link to stremer's discord
    @command(name='discord', aliases = ['Discord'])
    async def discord(self, ctx):
        message = get_discord()
        if message:
            await ctx.channel.send(message)

    # Send link to streamer's twitter
    @command(name='twitter', aliases = ['Twitter'])
    async def twitter(self, ctx):
        message = get_twitter()
        if message:
            await ctx.channel.send(message)

    # Shout-out user. Mod-only, used to acknowledge raids
    @command(name='so', aliases = ['SO', 'So', 'Shoutout', 'shoutout'])
    async def shoutout(self, ctx):
        if ctx.author.is_mod or util.is_vip(ctx.author.badges):
            message = get_shoutout(ctx)
        if message:
            await ctx.channel.send(message)

    # @command(name='mods', aliases = ['Mods'])
    # async def get_mods(self, ctx):
    #     message = get_mods(ctx)
    #     if message:
    #         await ctx.channel.send(message)

    @command(name='avorion', aliases = ['Avorion','ships','Ships'])
    async def link_avorion_profile(self, ctx):
        message = link_avorion()
        if message:
            await ctx.channel.send(message)

