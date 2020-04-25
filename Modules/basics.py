import botActions
import random
import util
import settings
from datetime import datetime
from twitch import TwitchHelix
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command

@cog()
class Basics:

    def get_commands(self):
        return 'Available Commands: !bot, !discord, !twitter, !avorion, !uptime, !tfcheck, !quote'

    def get_bot_info(self):
        return 'FoxBot is written in Python by @zielfoxx and @YorkRacc. !commands for available commands. Ideas/Feedback always welcome!'

    def get_uptime(self):
        # Set up twitch API call and get stream info
        client = TwitchHelix(client_id = settings.get_client_id())
        stream = client.get_streams(user_logins = settings.get_channel())._queue[0]
        # Get stream start time (API sends UTC time) and calculate uptime
        start_time = stream["started_at"]
        uptime = datetime.utcnow() - start_time
        return str(uptime).split(".")[0]

    def get_shoutout(self, ctx):
        response = ''
        if ctx.author.is_mod and util.validateName(ctx.content):
            name = ctx.content.split()[1][1:]
            response = 'Shoutout to ' + name + '! Check out their stream at twitch.tv/' + name + ' and give them a follow!'
        return response

    # Commands

    # List all general commands
    @command(name='commands', aliases=['help', 'Commands', 'Help'])
    async def list_commands(self, ctx):
        message = self.get_commands()
        await ctx.channel.send(message)

    # Post general info about the bot
    @command(name='bot', aliases=['info', 'Bot', 'Info'])
    async def bot_info(self, ctx):
        message = self.get_bot_info()
        await ctx.channel.send(message)

    # Get stream uptime. Responds with stream uptime
    @command(name='uptime', aliases = ['Uptime'])
    async def uptime(self, ctx):
        message = self.get_uptime()
        await ctx.channel.send(message)

    # Send link to stremer's discord
    @command(name='discord', aliases = ['Discord'])
    async def discord(self, ctx):
        message = settings.get_discord()
        await ctx.channel.send(message)

    # Send link to streamer's twitter
    @command(name='twitter', aliases = ['Twitter'])
    async def twitter(self, ctx):
        message = settings.get_twitter()
        await ctx.channel.send(message)

    # Shout-out user. Mod-only, used to acknowledge raids
    @command(name='so', aliases = ['SO', 'So', 'Shoutout', 'shoutout'])
    async def shoutout(self, ctx):
        message = self.get_shoutout(ctx)
        await ctx.channel.send(message)

