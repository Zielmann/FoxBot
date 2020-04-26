import random
import util
import settings
from datetime import datetime
from twitch import TwitchHelix
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command

def get_bot_info():
    return 'FoxBot is written in Python by @zielfoxx and @YorkRacc. !commands for available commands. Ideas/Feedback always welcome!'

def get_commands():
    return 'Available Commands: !bot, !discord, !twitter, !avorion, !uptime, !tfcheck, !quote, !mods'

def get_uptime():
    # Set up twitch API call and get stream info
    client = TwitchHelix(client_id = settings.get_client_id())
    stream = client.get_streams(user_logins = settings.get_channel())._queue[0]
    # Get stream start time (API sends UTC time) and calculate uptime
    start_time = stream["started_at"]
    uptime = datetime.utcnow() - start_time
    return str(uptime).split(".")[0]

def get_shoutout(ctx):
    response = ''
    if ctx.author.is_mod and util.validateName(ctx.content):
        name = ctx.content.split()[1][1:]
        response = 'Shoutout to ' + name + '! Check out their stream at twitch.tv/' + name + ' and give them a follow!'
    return response

def get_twitter():
    response = ''
    if settings.get_twitter():
        response = settings.get_twitter()
    return response

def get_discord():
    response = ''
    if settings.get_discord():
        response = settings.get_discord()
    return response

def get_mods(ctx):
    response = ''
    if util.checkGame(ctx, settings.get_client_id(), settings.get_channel(),'rimworld'):
        response = settings.get_rimworld_mods()
    elif util.checkGame(ctx, settings.get_client_id(), settings.get_channel(),'factorio'):
        response = settings.get_factorio_mods()
    return response

def link_avorion():
    response = 'Haurbus makes ships! Check them out here: ' + settings.get_avorion_link()
    return response

@cog()
class Basics:

    # Post general info about the bot
    @command(name='bot', aliases=['info', 'Bot', 'Info'])
    async def bot_info(self, ctx):
        message = get_bot_info()
        await ctx.channel.send(message)

    # List all general commands
    @command(name='commands', aliases=['help', 'Commands', 'Help'])
    async def list_commands(self, ctx):
        message = get_commands()
        await ctx.channel.send(message)

    # Get stream uptime. Responds with stream uptime
    @command(name='uptime', aliases = ['Uptime'])
    async def uptime(self, ctx):
        message = get_uptime()
        await ctx.channel.send(message)

    # Send link to stremer's discord
    @command(name='discord', aliases = ['Discord'])
    async def discord(self, ctx):
        message = get_discord()
        await ctx.channel.send(message)

    # Send link to streamer's twitter
    @command(name='twitter', aliases = ['Twitter'])
    async def twitter(self, ctx):
        message = get_twitter()
        await ctx.channel.send(message)

    # Shout-out user. Mod-only, used to acknowledge raids
    @command(name='so', aliases = ['SO', 'So', 'Shoutout', 'shoutout'])
    async def shoutout(self, ctx):
        message = get_shoutout(ctx)
        await ctx.channel.send(message)

    @command(name='mods', aliases = ['Mods'])
    async def get_mods(self, ctx):
        message = get_mods(ctx)
        await ctx.channel.send(message)

    @command(name='avorion', aliases = ['Avorion','ships','Ships'])
    async def link_avorion_profile(self, ctx):
        message = link_avorion()
        await ctx.channel.send(message)

