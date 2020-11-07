import util
import logging
import settings
import Modules
import asyncio
from twitchio.ext import commands

# Load settings from settings.xml
settings.load_settings()
chat_flag = True

# Set up basic logging handler
if settings.get_logging().lower() == 'debug':
    logLevel = logging.DEBUG
else:
    logLevel = logging.CRITICAL

logging.basicConfig(filename='FoxBot_log.txt', level=logLevel, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize twitchio command bot
bot = commands.Bot(
    irc_token = settings.get_app_token(),
    client_id = settings.get_client_id(),
    nick = settings.get_bot_account(),
    prefix = settings.get_prefix(),
    initial_channels = [settings.get_channel()]
)

#---------------------------------------------------#

async def start_periodic_messages():
    """
    Sends messages to chat periodically

    Period (in minutes) is defined in settings
    Checks for recent activity in chat before sending messages (prevents filling an inactive chat)
    If multiple messages are configured, they are distributed evenly across the specified period
    If no messages are configured, periodically checks if message has been added

    Parameters:
        messags: a list of strings
    """
    global chat_flag
    while True:
        messages = settings.get_periodic_messages()
        if messages:
            interval = 60 * int(settings.get_periodic_timer())
            ws = bot._ws
            if isinstance(messages, str):
                if chat_flag:
                    await ws.send_privmsg(settings.get_channel(), messages)
                    chat_flag = False
                await asyncio.sleep(interval)
            else:
                if chat_flag:
                    for m in messages:
                        interval = int((60 * int(settings.get_periodic_timer())) / len(messages))
                        if interval == 0:
                            interval = 1
                        await ws.send_privmsg(settings.get_channel(), m)
                        await asyncio.sleep(interval)
                    chat_flag = False
                else:
                    await asyncio.sleep(interval)
        else:
            await asyncio.sleep(60 * int(settings.get_periodic_timer()))

# Bot startup confirmation
@bot.event
async def event_ready():
    """
    Called once when the bot goes online.

    Sends a greeting message to the chat and then kicks off periodic messages, if any
    Periodic messages are defined in settings.xml
    """
    print(f"{settings.get_bot_account()} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(settings.get_channel(), f"/me is alive!")
    await start_periodic_messages()

# Read incoming messages
@bot.event
async def event_message(ctx):
    """
    Runs every time a message is sent in chat.
    """
    logging.debug('### NEW MESSAGE ###')
    logging.debug(ctx.content)
    logging.debug(ctx.author)
    global chat_flag
    # Sets chat flags to True for periodic messages and raffle reminders
    if ctx.author.name != settings.get_bot_account():
        chat_flag = True
        Modules.raffle.set_raffle_chat_flag()
    # Checks if message was part of a random tf redemption
    if 'custom-reward-id' in ctx.tags and ctx.tags['custom-reward-id'] == settings.get_random_tf_id():
        reply = Modules.tf.redeem_random(ctx)
        if reply:
            await ctx.channel.send(reply)
    # Checks if message was part of a direct tf redemption
    elif 'custom-reward-id' in ctx.tags and ctx.tags['custom-reward-id'] == settings.get_direct_tf_id():
        reply = Modules.tf.redeem_direct(ctx)
        if reply:
            await ctx.channel.send(reply)
    await bot.handle_commands(ctx)

#----------------------------------------------------#

@bot.command(name='setinterval', aliases=['Setinterval','SetInterval','setInterval'])
async def set_interval(ctx):
    """
    TwitchIO Bot Command

    Sets the interval used for periodic messages
    Available only to streamer/moderators
    New interval (in minutes) is to be provided along with the command, and must be a number

    Parameters:
        ctx: TwitchIO message context
    """
    if ctx.author.is_mod:
        interval = ctx.content.split()[1]
        try:
            int(interval)
            settings.set_periodic_timer(interval)
            message = 'Updated message interval to ' + interval + ' minutes'
        except:
            message = 'Could not update message interval'
        if message:
            await ctx.channel.send(message)

@bot.command(name='addmessage', aliases=['addMessage', 'AddMessage', 'Addmessage'])
async def add_message(ctx):
    """
    TwitchIO Bot Command

    Adds a new periodic message to the queue
    Available only to streamer/moderators
    New message is to be provided along with the command

    Parameters:
        ctx: TwitchIO message context
    """
    if ctx.author.is_mod:
        message = ' '.join(map(str,ctx.content.split()[1:]))
        if message:
            settings.add_periodic_message(message)
            await ctx.channel.send('Added message: ' + message)
        else:
            await ctx.channel.send('No message provided')


#----------------------------------------------------#

if __name__ == "__main__":
    print('FoxBot starting...\n')
    print('If bot welcome message does not appear, the app_token in settings.xml may be incorrect or may have changed. ' + 
        'Please go back through the setup steps found in the README to make sure the app_token and client_id are up-to-date ' + 
        'and that FoxBot is properly connected to your Twitch account.\n')
    if settings.basics_enabled():
        bot.load_module('Modules.basics')
    if settings.raffle_enabled():
        bot.load_module('Modules.raffle')
    if settings.quotes_enabled():
        bot.load_module('Modules.quotes')
    if settings.emotes_enabled():
        bot.load_module('Modules.emotes')
    if settings.tf_enabled():
        bot.load_module('Modules.tf')
    if settings.rimworld_enabled():
        bot.load_module('Modules.rimworld')
    if settings.counter_enabled():
        bot.load_module('Modules.counter')
    bot.run()   
