import random
import settings
import util
import os
import json
from datetime import datetime
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command


def load_quotes():
    quotes = {}
    if os.path.isfile('quotes.json') and os.path.getsize('quotes.json') != 0:
        with open('quotes.json', 'r') as json_file:
            quotes = json.load(json_file)
    return quotes

quotes = load_quotes()

def save_quotes(quote_dict):
    with open('quotes.json', 'w') as json_file:
        json.dump(quote_dict, json_file, indent=4)
    return

def add(ctx):
    response = ''
    if ctx.author.is_mod:
        # Puts provided quote into a single string, without including the '!addquote' at the start
        quote = ' '.join(map(str,ctx.content.split()[1:]))
        if quote:
            today = datetime.today()
            date = str(today.day) + '/' + str(today.month) + '/' + str(today.year)
            # If no stored quotes, sets first entry as quote number 1. Otherwise adds one to the last key in quotes (the last quote number)
            if len(quotes) == 0:
                number = '1'
            else:
                number = str(int(list(quotes.keys())[-1]) + 1)
            game = util.getGameName(ctx,settings.get_client_id(),settings.get_channel())
            # Build dictionary to associate date and game with the quote
            raw_quote = {
                "date": date,
                "quote": quote,
                "game": game
                }
            quotes[number] = raw_quote
            save_quotes(quotes)
            response = str(number) + ': ' + quotes[number]["quote"] + ' - while playing ' + quotes[number]["game"] + ' on ' + quotes[number]["date"]
    return response

def remove(ctx):
    response = ''
    if ctx.author.is_mod:
        # If quote number is given, removes quote from list
        content = ctx.content.split()
        if len(content) > 1:
            number = content[1]
            if number in quotes:
                removed = quotes.pop(number)
                save_quotes(quotes)
                response = 'Deleted ' + number + ': ' + removed["quote"]
    return response

def edit(ctx):
    response = ''
    if ctx.author.is_mod:
        content = ctx.content.split()
        if len(content) > 1:
            number = content[1]
            # Creates string of updated quote, without !ediquote command or quote number
            new_quote = ' '.join(map(str,content[2:]))
            if new_quote and number in quotes:
                quotes[number]["quote"] = new_quote
                save_quotes(quotes)
                response = 'Updated ' + number + ': ' + quotes[number]["quote"]
    return response

def search(ctx):
    response = ''
    # Search string is anything provided after the !quote command
    search = ' '.join(map(str,ctx.content.split()[1:]))
    # If search was just a valid quote number, returns that quote
    if search in quotes:
        response = str(search) + ': ' + quotes[search]["quote"] + ' - while playing ' + quotes[search]["game"] + ' on ' + quotes[search]["date"]
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
            response = str(results[number]) + ': ' + selected["quote"] + ' - while playing ' + selected["game"] + ' on ' + selected["date"]
    return response


@cog()
class Quotes:

    @command(name='addquote', aliases = ['Addquote', 'quoteadd', 'Quoteadd'])
    async def add_quote(self, ctx):
        message = add(ctx)
        await ctx.channel.send(message)

    @command(name='quote', aliases = ['Quote'])
    async def get_quote(self, ctx):
        message = search(ctx)
        await ctx.channel.send(message)

    @command(name='editquote', aliases = ['Editquote', 'quoteedit', 'Quoteedit'])
    async def edit_quote(self, ctx):
        message = edit(ctx)
        await ctx.channel.send(message)

    @command(name='removequote', aliases = ['Removequote','deletequote','Deletequote','rmquote'])
    async def remove_quote(self, ctx):
        message = remove(ctx)
        await ctx.channel.send(message)

