import util
import logging
import settings
import Modules
import asyncio
from twitchio.ext import commands

# Load settings from settings.xml
settings.load_settings()
chat_flag = False

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

async def start_periodic_messages(messages):
    """
    Sends messages to chat periodically

    Period (in minutes) is defined in settings
    Checks for recent activity in chat before sending messages (prevents filling an inactive chat)
    If multiple messages are specified, they are distributed evenly across the specified period

    Parameters:
        messags: a list of strings
    """
    while True:
        global chat_flag
        interval = base_time = 60 * int(settings.get_periodic_timer())
        ws = bot._ws
        if isinstance(messages, str):
            if chat_flag:
                await ws.send_privmsg(settings.get_channel(), messages)
                chat_flag = False
            await asyncio.sleep(interval)
        else:
            if chat_flag:
                interval = int(base_time / len(messages))
                for m in messages:
                    await ws.send_privmsg(settings.get_channel(), m)
                    await asyncio.sleep(interval)
                chat_flag = False
            else:
                await asyncio.sleep(interval)

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
    messages = settings.get_periodic_messages()
    if messages:
        await start_periodic_messages(messages)

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

if __name__ == "__main__":
    print('FoxBot starting...\n')
    print('If bot welcome message does not appear, the app_token in settings.xml may be incorrect or may have changed. ' + 
        'Please go back through the setup steps found in the README to make sure the app_token and client_id are up-to-date ' + 
        'and that FoxBot is properly connected to your Twitch account.\n')
    bot.load_module('Modules.basics')
    bot.load_module('Modules.raffle')
    bot.load_module('Modules.quotes')
    bot.load_module('Modules.emotes')
    bot.load_module('Modules.tf')
    bot.load_module('Modules.rimworld')
    bot.run()   
