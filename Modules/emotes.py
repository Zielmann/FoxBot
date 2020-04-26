
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
