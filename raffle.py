import botActions
import random
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command

@cog()
class Raffle:
    
    raffle = []
    active = False

    def pick(self, ctx):
        response = ''
        if self.active and ctx.author.is_mod:
            if  not self.raffle:
                response = 'There are no entries in the raffle'
            else:
                # Picks winner from raffle list, first entry (raffle status) is excluded
                winner = random.choice(self.raffle)
                response = 'Contratulations @' + winner + ', you won the raffle!'
                self.raffle.remove(winner)
        elif not self.active and ctx.author.is_mod:
            response = 'There is no active raffle'
        return response

    def enter(self, ctx):
        response = ''
        # Enters user in raffle if raffle is active
        if self.active:
            name = ctx.author.name
            # Make sure user has not already entered
            if not name in self.raffle:
                self.raffle.append(name)
                response = name + ' has entered the raffle!'
        return response

    def start(self, ctx):
        response = ''
        # Sets raffle status to True
        if not self.active and ctx.author.is_mod:
            self.active = True
            response = 'A raffle has been started! Use !raffle to enter!'
        return response

    def end(self, ctx):
        response = ''
        # If raffle is active, clears all entires and sets raffle status to False
        if self.active and ctx.author.is_mod:
            self.active = False
            self.raffle = []
            response = 'The raffle has been closed'
        return response

    # Pick winner from raffle list. Mod-only
    @command(name='draw', aliases = ['Draw', 'pick', 'Pick'])
    async def raffle_pick(self, ctx):
        message = self.pick(ctx)
        await ctx.channel.send(message)

    # Enter user into raffle list
    @command(name='raffle', aliases = ['Raffle'])
    async def enter_raffle(self, ctx):
        message = self.enter(ctx)
        await ctx.channel.send(message)

    # Start a raffle. Mod-only
    @command(name='startraffle', aliases = ['Startraffle', 'rafflestart', 'Rafflestart'])
    async def start_raffle(self, ctx):
        message = self.start(ctx)
        await ctx.channel.send(message)

    # End a raffle. Mod-only
    @command(name='endraffle', aliases = ['Endraffle', 'raffleend', 'Raffleend'])
    async def end_raffle(self, ctx):
        message = self.end(ctx)
        await ctx.channel.send(message)

