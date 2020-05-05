import random
import asyncio
import settings
from datetime import datetime
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command

raffle_chat_flag = False

def set_raffle_chat_flag():
    global raffle_chat_flag
    raffle_chat_flag = True

@cog()
class Raffle:
    
    # Variables
    raffle = []
    active = False

    def pick(self, ctx):
        """
        Picks a random entry and removes them from the raffle.

        Parameters:
            ctx: The context of the message

        Returns 
            str: Contains the winner of the raffle
        """
        response = ''
        if self.active and ctx.author.is_mod:
            if not self.raffle:
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
        """
        Adds a user to the raffle if they have not already entered

        Parameters:
            ctx: The context of the message

        Returns:
            str: Confirms the username of the user that is entered
        """
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
        """
        Activates the raffle for entries

        Parameters:
            ctx: The context of the message

        Returns:
            str: confirms the raffle has started
        """
        response = ''
        # Sets raffle status to True
        if not self.active and ctx.author.is_mod:
            self.active = True
            response = 'A raffle has been started! Use !raffle to enter!'
        return response

    def end(self, ctx):
        """
        Ends the raffle and clears the entires

        Parameters:
            ctx: The context of the message

        Returns:
            str: confirms the raffle has been closed
        """
        response = ''
        # If raffle is active, clears all entires and sets raffle status to False
        if self.active and ctx.author.is_mod:
            self.active = False
            self.raffle = []
            response = 'The raffle has been closed'
        return response

    async def raffle_reminder(self, ctx):
        """
        Periodically sends reminder that raffle is active

        Period is defined in settings.xml, in minutes
        Checks for recent chat activity before sending (prevents filling an inactive chat)
        Parameters:
            ctx: the context of the message
        """
        global raffle_chat_flag
        base_time = settings.get_raffle_reminder_interval()
        if base_time:
            interval = 60 * int(settings.get_raffle_reminder_interval())
            while self.active:
                await asyncio.sleep(interval)
                if self.active and raffle_chat_flag: # Makes sure raffle is still active after sleep expires
                    raffle_chat_flag = False
                    await ctx.channel.send('A raffle is active! Use !raffle to enter!')

    # Commands

    # Pick winner from raffle list. Mod-only
    @command(name='draw', aliases = ['Draw', 'pick', 'Pick'])
    async def raffle_pick(self, ctx):
        message = self.pick(ctx)
        if message:
            await ctx.channel.send(message)

    # Enter user into raffle list
    @command(name='raffle', aliases = ['Raffle'])
    async def enter_raffle(self, ctx):
        message = self.enter(ctx)
        if message:
            await ctx.channel.send(message)

    # Start a raffle and kick off raffle reminders. Mod-only
    @command(name='startraffle', aliases = ['Startraffle', 'rafflestart', 'Rafflestart'])
    async def start_raffle(self, ctx):
        message = self.start(ctx)
        if message:
            await ctx.channel.send(message)
            await self.raffle_reminder(ctx)

    # End a raffle. Mod-only
    @command(name='endraffle', aliases = ['Endraffle', 'raffleend', 'Raffleend'])
    async def end_raffle(self, ctx):
        message = self.end(ctx)
        if message:
            await ctx.channel.send(message)
