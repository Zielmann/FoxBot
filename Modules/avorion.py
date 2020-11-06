import settings
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command

def link_avorion():
    response = settings.get_avorion_link()
    return response

@cog
class Avorion:

    @command(name='avorion', aliases = ['Avorion','ships','Ships'])
    async def link_avorion_profile(self, ctx):
        message = link_avorion()
        if message:
            await ctx.channel.send(message)

