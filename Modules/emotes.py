from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command

"""
To create a new emote follow these steps:
1.  Add a new method under "Available Emotes",
    make it return a string containing the emote
    you would like the bot to display.

2.  Add an @command with the "name" argument,
    set the name = the chat command for the emote.
    Create another method under the command and call
    your first method from (1), then use 
    ctx.channel.send(message) to send your emote to the chat.
"""

# Available Emotes
def oof():
    return 'haurbuOof haurbuOof haurbuOof'

def heart():
    return 'haurbuHeart haurbuHeart haurbuHeart'

@cog()
class Emotes:

    @command(name='Oof')
    async def oof(self, ctx):
        message = oof()
        if message:
            await ctx.channel.send(message)

    @command(name='Heart')
    async def heart(self, ctx):
        message = heart()
        if message:
            await ctx.channel.send(message)

    # Used to prevent nuisance output to the terminal when message starts with streamer's name
    # In this case, streamer is haurbus, and emotes are prefixed with 'haurbu'
    @command(name='s')
    async def do_nothing(self, ctx):
        pass
