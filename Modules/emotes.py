from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command

def oof():
    return 'haurbuOof haurbuOof haurbuOof'

def heart():
    return 'haurbuHeart haurbuHeart haurbuHeart'

@cog()
class Emotes:

    @command(name='Oof')
    async def oof(self, ctx):
        message = oof()
        await ctx.channel.send(message)

    @command(name='Heart')
    async def heart(self, ctx):
        message = heart()
        await ctx.channel.send(message)

    # Used to prevent nuisance output to the terminal when message starts with streamer's name
    # In this case, streamer is haurbus, and emotes are prefixed with 'haurbu'
    @command(name='s')
    async def do_nothing(self, ctx):
        await ctx.channel.send('')
