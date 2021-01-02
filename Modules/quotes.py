import random
import settings
import util
import os
import json
from datetime import datetime
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command


def load_quotes():
    """
    Loads a dict of quotes by id from "Data/quotes.json"

    Returns:
        dict: Contains quotes by id
    """
    quotes = {}
    if os.path.isfile('Data/quotes.json') and os.path.getsize('Data/quotes.json') != 0:
        with open('Data/quotes.json', 'r') as json_file:
            quotes = json.load(json_file)
    return quotes

quotes = load_quotes()

def save_quotes(quote_dict):
    """
    Writes the passed dict of quotes to "Data/quotes.json"

    Parameters:
        quote_dict: The current dictionary of quotes to write
    """
    with open('Data/quotes.json', 'w') as json_file:
        json.dump(quote_dict, json_file, indent=4)
    return

def add(ctx):
    """
    Adds a quote from the content of the message to the current quotes

    Parameters:
        ctx: The context of the message

    Returns:
        str: The quote which has been added 
    """
    response = ''
    if ctx.author.is_mod or (settings.vip_quotes_allowed() and util.is_vip(ctx.author.badges)):
        # Puts provided quote into a single string, without including the '!addquote' at the start
        msg = ' '.join(map(str,ctx.content.split()[1:]))
        if msg:
            today = datetime.today()
            date = str(today.day) + '/' + str(today.month) + '/' + str(today.year)
            # If no stored quotes, sets first entry as quote number 1. Otherwise adds one to the last key in quotes (the last quote number)
            if len(quotes) == 0:
                number = '1'
            else:
                number = str(int(list(quotes.keys())[-1]) + 1)
            game = util.getGameName(ctx, settings.get_client_id(), settings.get_client_secret(), settings.get_channel())
            quote = msg
            # Build dictionary to associate date and game with the quote
            raw_quote = {
                "date": date,
                "quote": quote,
                "game": game
                }
            quotes[number] = raw_quote
            save_quotes(quotes)
            response = f"{number}: {quotes[number]['quote']} - while streaming {quotes[number]['game']} on {quotes[number]['date']}"
    return response

def remove(ctx):
    """
    Removes a quote by the Id number in message content

    Parameters:
        ctx: The context of the message

    Returns:
        str: Confirmation of the deleted quote's id and content
    """
    response = ''
    if ctx.author.is_mod:
        # If quote number is given, removes quote from list
        content = ctx.content.split()
        if len(content) > 1:
            number = content[1]
            if number in quotes:
                removed = quotes.pop(number)
                save_quotes(quotes)
                response = f"Deleted {number}: {removed['quote']}"
    return response

def edit(ctx):
    """
    Edits a quote by the Id number in the message content

    Parameters:
        ctx: The context of the message
        
    Returns:
        str: Confirmation of the edited quote's id and content
    """
    response = ''
    if ctx.author.is_mod:
        content = ctx.content.split()
        if len(content) > 1:
            number = content[1]
            # Creates string of updated quote, without !ediquote command or quote number
            new_quote = ' '.join(map(str,content[2:]))
            if new_quote.lower().startswith('game:') and number in quotes:
                new_game = new_quote[new_quote.lower().index("game:")+len("game:"):]
                quotes[number]["game"] = new_game
                save_quotes(quotes)
                response = f"Updated quote {number} game to: {quotes[number]['game']}"
            elif new_quote and number in quotes:
                if 'game:' in new_quote.lower():
                    new_game = new_quote[new_quote.lower().index("game:")+len("game:"):].strip()
                    new_quote = new_quote[:new_quote.lower().index("game:")].strip()                 
                    quotes[number]["quote"] = new_quote
                    quotes[number]["game"] = new_game
                    response = f"Updated {number}: {quotes[number]['quote']} - while streaming {quotes[number]['game']} on {quotes[number]['date']}"
                else:
                    quotes[number]["quote"] = new_quote
                    response = f"Updated {number}: {quotes[number]['quote']} - while streaming {quotes[number]['game']} on {quotes[number]['date']}"
                save_quotes(quotes)
    return response

def search(ctx):
    """
    Searches for a quote by the Id number or terms in the context
    If the search terms match multiple quotes one is randomly chosen

    Parameters:
        ctx - The context of the message

    Returns:
        str: A quote which matches the search critera
    """
    response = ''
    # Search string is anything provided after the !quote command
    search = ' '.join(map(str,ctx.content.split()[1:]))
    # If search was just a valid quote number, returns that quote
    if search in quotes:
        response = f"{search}: {quotes[search]['quote']} - while streaming {quotes[search]['game']} on {quotes[search]['date']}"
    else:
        results = []
        # Find all quotes containing provided search term
        for item in quotes:
            if search.lower() in quotes[item]["quote"].lower():
                results.append(item)
        if results:
            # Chooses a random quote from the list of results
            number = random.randrange(len(results))
            selected = quotes[results[number]]
            response = f"{results[number]}: {selected['quote']} - while streaming {selected['game']} on {selected['date']}"
    return response


@cog()
class Quotes:

    @command(name='addquote', aliases = ['Addquote', 'quoteadd', 'Quoteadd'])
    async def add_quote(self, ctx):
        message = add(ctx)
        if message:
            await ctx.channel.send(message)

    @command(name='quote', aliases = ['Quote'])
    async def get_quote(self, ctx):
        message = search(ctx)
        if message:
            await ctx.channel.send(message)

    @command(name='editquote', aliases = ['Editquote', 'quoteedit', 'Quoteedit'])
    async def edit_quote(self, ctx):
        message = edit(ctx)
        if message:
            await ctx.channel.send(message)

    @command(name='removequote', aliases = ['Removequote','deletequote','Deletequote','rmquote'])
    async def remove_quote(self, ctx):
        message = remove(ctx)
        if message:
            await ctx.channel.send(message)

