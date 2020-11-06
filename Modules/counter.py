import settings
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command

active_counts = {}

def get_counter_and_value(ctx):
    """
    Separates text and numbers from message

    Parameters:
        ctx: the full context of the message

    Returns:
        str, int
    """
    msg = ' '.join(map(str,ctx.content.split()[1:])).lower()
    value = [int(i) for i in msg.split() if i.isdigit()]
    if value:
        counter = msg.split(str(value[0]))[0].strip().lower()
        value = value[0]
    else:
        counter = msg
    return counter, value

@cog()
class Count:

    @command(name='newcount', aliases=['Newcount', 'NewCount'])
    async def add_counter(self, ctx):
        """
        Starts a new counter if a counter name is provided and it is not already in use
        If a value is provided after the counter name, counter will start with the specified value. 
        Otherwise new counter value defaults to 0
        """
        if ctx.author.is_mod:
            new_counter, value = get_counter_and_value(ctx)
            if not new_counter:
                message = "Must provide a counter name"
            elif new_counter in active_counts:
                message = f"Already counting {new_counter}"
            else:
                if value:
                    active_counts[new_counter] = value
                else:
                    active_counts[new_counter] = 0
                message = f"Now counting {new_counter}!"
            await ctx.channel.send(message)

    @command(name='count', aliases=['Count'])
    async def show_count(self, ctx):
        """
        If specified count is active, responds with the count's current value
        If no count specified, responds with a list of all active counts
        """
        counter = get_counter_and_value(ctx)[0]
        if active_counts and not counter:
            message = ' | '.join([f'{key}: {value}' for key, value in active_counts.items()])
            await ctx.channel.send(message)
        elif counter in active_counts:
            message = f"Total {counter}: {active_counts[counter]}"
            await ctx.channel.send(message)

    @command(name='add', aliases=['Add'])
    async def incrememnt_counter(self,ctx):
        """
        If value is provided after the counter name, increments the counter by the given value
        Otherwise increments the counter by one
        """
        if ctx.author.is_mod:
            counter, value = get_counter_and_value(ctx)
            if counter in active_counts:
                if value:
                    active_counts[counter] += value
                else:
                    active_counts[counter] += 1
                message = f"Total {counter}: {active_counts[counter]}"
                await ctx.channel.send(message)

    @command(name='set', aliases=['Set'])
    async def set_counter(self,ctx):
        """
        If value is provided after the counter name, sets the counter to the given value
        """
        if ctx.author.is_mod:
            counter, value = get_counter_and_value(ctx)
            if value and counter in active_counts:
                active_counts[counter] = value
                message = f"Total {counter}: {active_counts[counter]}"
                await ctx.channel.send(message)

    @command(name='reset', aliases=['Reset'])
    async def reset_counter(self,ctx):
        """
        If counter is active, sets the counter's value to zero
        """
        if ctx.author.is_mod:
            counter = get_counter_and_value(ctx)[0]
            if counter in active_counts:
                active_counts[counter] = 0
                message = f"Total {counter}: {active_counts[counter]}"
                await ctx.channel.send(message)

    @command(name='endcount', aliases=['Endcount', 'EndCount'])
    async def remove_counter(self,ctx):
        """
        If given counter is active, removes the counter
        """
        if ctx.author.is_mod:
            counter = get_counter_and_value(ctx)[0]
            if counter in active_counts:
                active_counts.pop(counter)
                message = f"Stopped counting {counter}"
                await ctx.channel.send(message)
