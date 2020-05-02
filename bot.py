import util
import logging
import settings
import Modules
from twitchio.ext import commands

# Load settings from settings.xml
settings.load_settings()

# Set up basic logging handler
if settings.get_logging().lower() == 'debug':
    logLevel = logging.DEBUG
else:
    logLevel = logging.CRITICAL

logging.basicConfig(filename='FoxBot_log.txt', level=logLevel, format='%(asctime)s - %(levelname)s - %(message)s')


# Initialize twitchio command bot
bot = commands.Bot(
    irc_token= settings.get_app_token(),
    client_id= settings.get_client_id(),
    nick= settings.get_bot_account(),
    prefix= settings.get_prefix(),
    initial_channels=[settings.get_channel()]
)

#---------------------------------------------------#

# Bot startup confirmation
@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{settings.get_bot_account()} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(settings.get_channel(), f"/me is alive!")

# Read incoming messages
@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'
    logging.debug('### NEW MESSAGE ###')
    logging.debug(ctx.content)
    logging.debug(ctx.author)
    if 'custom-reward-id' in ctx.tags and ctx.tags['custom-reward-id'] == settings.get_random_tf_id():
        reply = Modules.tf.redeem_random(ctx)
        await ctx.channel.send(reply)
    elif 'custom-reward-id' in ctx.tags and ctx.tags['custom-reward-id'] == settings.get_direct_tf_id():
        reply = Modules.tf.redeem_direct(ctx)
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
