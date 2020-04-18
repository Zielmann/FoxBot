# FoxBot
FoxBot is a Twitch bot built off of twitchio for Twitch chat interaction and TwitchHelix for Twitch API access. This bot supports some common chat commands as well as a custom 'TF' feature, which allows for transforming viewers into various animals, objects... or anything else you want! It is also capable of responding to emotes and channel point reward redemptions.

## General Commands:

!bot, !info
Displays basic info about FoxBot

!commands, !help
Lists general commands that can be used by anybody (no mod/streamer -only commands)

!uptime
Displays how long stream has been live

!discord
Displays streamer's Discord

!twitter
Displays streamer's Twitter

!so @username, !shoutout @username
Gives a shoutout to specified user, linking their twitch channel

!startraffle
Streamer and moderator only. After starting a raffle, users will be able to enter the raffle

!raffle
Enters user into raffle list. Raffle list will be empty when the bot starts

!draw, !pick
Streamer and moderator only. Selects a random user from the raffle list, and removes them from the list

!endraffle
Streamer and moderator only. Ending the raffle will remove all entires from the raffle. After raffle is ended, entering the raffle will be disabled

!addquote {quote}
Streamer and moderator only. Adds quote to list. List is stored in quotes.json file. Date and game data are both stored along with the quote

!quote {quote number} OR {search term}
If valid quote number is provided, will return the corresponding quote
If search term is provided, will return a quote containing the search term. If multiple contain the search term, picks a random quote from the list of matches

!editquote {quote number} {new quote}
Streamer and moderator only. Updates the specified quote with the provided new quote text. Allows for fixing typos, etc.

!removequote {quote number}
Streamer and moderator only. Removes the specified quote from the list

!tfcheck
Displays current species of user who sent the command

!mods
Displays list of mods for current game (currently supports Rimworld and Factorio)

!tf {username} {species}(optional)
Streamer and moderator only. Streamer has the option to specify the species, while mods do not. If no species provided, assigns the user a random species from species.txt file. User and species pair is then recorded in tfList.csv. This can also be set up to occur when a viewer redeems a custom reward with channel points. See Channel Points Integration below.

!revert {username}
Moderator only. Reverts specified user back into a human

!avorion, !ships
Provides link to Avorion Steam Workshop profile

## Rimworld Commands: (only available when streaming rimworld)

!rimworld
Displays all Rimworld commands. 

!item {itemName}, !items {itemName}
Displays info on a Rimworld item

!event {eventName}, !events {itemName}
Displays info on a Rimworld event

## Raffle Feature

FoxBot contains a simple raffle feature. Raffle is inactive by default. The streamer and moderators can start a raffle, end the current raffle, and have the bot randomly select a winner from the list. The winner will be removed from the list, but currently nothing prevents them from simply re-entering the raffle. Raffle entries are NOT saved, so each time the bot is started it will have an empty raffle list. Ending the raffle will also clear the list of entries.

## Quote Feature

Stores and recalls quotes. Quotes can be added by the streamer and moderators. When a quote is added, it will also store the data and current game along with the quote. 
The streamer and moderators are also able to delete or modify saved quotes (allows correcting for typos, etc).
Any viewer can lookup a quote. Lookup can be done by specific quote number or by providing a search term. If there are multiple matches for the search term, the bot
will randomly select which match to return.

## Emote Responses

The bot can respond to emotes as if they are commands. Currently, handling for each emote must be individually implemented in the code.

## Channel Points Integration

Current implementation is a workaround, requiring the viewer to provide a message along with this event. This means the streamer must configure the event to require message input when redeemed. The message is checked for the specific custom-reward-id in the tags matching that of the reward being redeemed. Current supported redemptions are for random TF and direct TF rewards.

## Bot Setup
You will need to update the settings.xml file for the bot to run correctly. The following will walk you through the steps to get the required values for the empty fields. The ones already containing a value can be left alone. Before starting, make sure to have two-factor authentication enabled on the account the bot will be running from.

### App_token
This is what allows the bot to connect to Twitch chat. Log in to the account you want the bot to show up as in chat, and then go to https://twitchapps.com/tmi/ and click Connect. This will bring up a prompt to authorize the Twitch Chat OAuth Token Generator to access your account. Click Authorize, and it will generate an OAuth password for the bot. Copy the password shown, and add it as the app_token in settings.xml

### Client_id
This allows the bot to make calls to the Twitch API. You receive a client_id by registering the bot with twitch. While still logged in to the bot account, go to https://dev.twitch.tv/console/apps. This may prompt you to authroize Twitch Developer to access your account. Click Authorize. Next, click Register Your Application on the right. Give the app a name (can be anything, but cannot containt 'twitch' in any way). For the OAuth Redirect URLs field, add https://twitchapps.com/tokengen/ . In the Category drop-down, select Chat Bot. Now, click on Create and it will return to the Applications list. Now click on Manage for your new application, scroll down, and your client_id will be available. Copy this client_id and add it to the settings.xml

Now, navigate to https://twitchapps.com/tokengen/. It'll open the Twitch OAuth Token Generator. Paste that same client_id into the Client ID field. For Scopes, enter 'chat:edit chat:read whispers:edit whispers:read'. Then click on the broken icon beneath the redirect URL. This will bring up a prompt to authorize the application to access your account. Click Authorize at the bottom of the page. If you see a page with "Your OAuth Token" on it, this step is complete. You do not need to copy this token or add it to the settings.xml

### Bot_account
This is the name of the twitch account the bot runs from. This should be the account you were logged into for generating the App_token and the Client_id

### Channel
This tells the bot what channel's chat to join. Enter your streaming channel name.

### Social Media
Any text you enter for the Twitter and Discord settings will be how the bot responds to the !twitter and !discord commands.

### Rimworld Settings

#### Mods
Any text you enter here will be how the bot responds to the !mods command when streaming Rimworld

#### Event_file
This specifies where the Rimworld Twitch Integration mod stores the list of events. This is usually stored in C:\Users\\<username\>\AppData\LocalLow\Ludeon Studios\RimWorld by Ludeon Studios\TwitchToolkit\StoreIncidents.json. If you don't see the AppData folder under your username, click on View in file explorer and check the 'Hidden Items' box. You can also find the directory by searching "TwitchToolkit" in file explorer, but this may take a while to give a result. You need to enter the full path to the StoreIncidents.json file in settings.xml.

#### Item_file
Same as Event_file, only add the full path to StoreItems.json. This should be in the same directory as the StoreIncidents.json file.

### Factorio Settings

#### Mods
Any text you enter here will be how the bot responds to the !mods command when streaming Factorio

### Avorion Settings

#### Profile_Link
Link to Steam Workshop profile for Avorion

### Custom Rewards
Sets the custom reward IDs to react to when somebody redeems a custom reward with channel points


References:

https://twitchio.readthedocs.io/en/rewrite/twitchio.html#client

https://python-twitch-client.readthedocs.io/en/latest/basic_usage.html

https://github.com/TwitchIO/TwitchIO/blob/master/twitchio/ext/commands/bot.py
