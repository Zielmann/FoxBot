<h1 align="center">FoxBot</h1>
<p align="center">
    A Twitch chat bot built in Python
    <br />
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Set Up the Bot](#set-up-the-bot)
  * [Run the Bot](#run-the-bot)
* [Usage](#usage)
  * [Adding a Feature Module](#adding-a-feature-module)
  * [Reacting to Channel Reward Redemptions](#reacting-to-channel-reward-redemptions)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgements](#acknowledgements)

<!-- ABOUT THE PROJECT -->
## About The Project

FoxBot started off as a project to put together a Twitch chat bot for a friend, so much of the initial functionality was built for his specific use in mind. As it has expanded, a few others have shown interest in using the bot or at least seeing how it's put together. So now it's public so others can use it as an example, run it themselves, or even help add more features!

### Built With

* [TwitchIO](https://twitchio.readthedocs.io/en/rewrite/)
* [Python-twitch-client (Twitch Helix)](https://python-twitch-client.readthedocs.io/en/latest/helix.html)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites

FoxBot was written with Python 3.8. It should be compatible with Python 3.6 or above, but it has not been tested on those earlier releases.

### Installation

1. Clone the repo

```sh
git clone https://github.com/Zielmann/FoxBot.git
```

2. Install required packages

```sh
pip install -r requirements.txt
```

### Set Up the Bot

To get the bot running, first you will need to do a little setup with Twitch and in the bot's settings.xml file.

#### Set Up Bot Account and Channel

FoxBot can either be run from the streaming account or from a secondary account. If a secondary account is preferred, be sure to add it as a moderator for your channel.

In the settings.xml file, add the channel name and the bot_account. For example, if you're streaming on FoxBotStream and the bot is running from FoxBotStreamBot, you would fill in the settings.xml like this:

```xml
        <bot_account>FoxBotStreamBot</bot_account>
        <channel>FoxBotStream</channel>
```

#### Twitch IRC Connection Setup

FoxBot requires an OAuth token to be able to connect to the Twitch IRC interface. You will need to generate an OAuth token and add it under app_token in the settings.xml file.

1. Log in to the Twitch account you want the bot to run from

2. Go to <https://twitchapps.com/tmi/> and click on Connect

3. You will be prompted to authorize the OAuth Token Generator to access your Twitch account. Click on Authorize.

4. Copy the full token, including the oauth: prefix, and add it to the settings.xml file

```xml
        <app_token>paste full oauth token here</app_token>
```

#### Twitch API Connection Setup

Foxbot needs to be registered as an application with Twitch and granted access to your Twitch account in order to be able to make calls to the Twitch API. During this process, a Client_ID will be generated, and you will be adding that to the settings.xml file.

1. While still logged in to the same Twitch account as before, go to <https://dev.twitch.tv/console/apps> (If prompted, authorize Twitch Developer to access your account)

2. In the developer console, click Applications

3. Click the Register Your Application button on the right

4. Give the app a name. This can be whatever you want, but cannot include 'twitch' in any form

5. In the OAuth Redirect URLs field, add <https://twitchapps.com/tokengen/>

6. Under Category, select Chat Bot from the dropdown and then click on Create

7. You should now see your application in the list of Developer Applications. Click on Manage on the right

8. You will see a Client ID field for your application. Copy that ID and add to the settings.xml file

```xml
        <client_id>paste application Client ID here</client_id>
```

9. Beneath the Client ID on the Twitch Dev Console, you will also see a Client Secret. If the value is displayed, copy it. If not, click the New Secret button, then click OK to accept generating a new secret. Copy the value shown and add it to the settings.xml file. Be sure to keep the client secret... secret!

```xml
        <client_secret>paste application Client Secret here</client_secret>
```

10. Go to <https://twitchapps.com/tokengen/> to bring up the Twitch OAuth Token Generator

11. Paste the application Client ID into the Client ID field

12. Copy and paste the following into the Scopes field

```
chat:edit chat:read whispers:edit whispers:read
```

13. Click on the broken icon image to generate the token. This should prompt you to authroize the application to access your Twitch account. Click Authorize

14. Now you should see a page with an OAuth token on it. This means the API connection setup is complete. You do not need to copy this token

### Run the Bot

You're now ready to start up the bot. When it's successfully running, the terminal will indicate the bot's account is online, and the bot will send a message to the stream chat.

Try sending !bot or !commands in chat, and the bot should respond!

<!-- USAGE EXAMPLES -->
## Usage

### Adding a Feature Module

FoxBot makes use of twitchio's Cog class decorator, which makes it easy to create modules for new features.

To make a new module, first start by creating a new file in the Modules folder. Be sure to import the Cog and Command decorators from twitchio.

```python
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command
```

Next, add a class with the Cog decorator. For example, you could write a feature to greet users in chat.

```python
@cog
class Greetings:
```

Then add commands to be included in the module.

```python
@command(name='hi')
async def say_hi(self, ctx):
    await ctx.channel.send('Hello!')
```

The command name is what you would use to trigger that command. So in this case sending '!hi' in the chat will make the bot send 'Hello!' back.

The argument 'ctx' is the context of the message containing the command. This contains things such as the contents of the message, the name of the sender, the name of the channel, and more. So if you wanted to make the bot's response a bit more personalized, you could get the name of the user who sent the command, and insert it into the response string.

```python
    await ctx.channel.send('Hello ' + ctx.author.name + '!')
```

Putting those together, you would end up with a greetings.py file containing:

```python
from twitchio.ext.commands.core import cog
from twitchio.ext.commands.core import command

@cog
class Feature:

    @command(name='hi')
    async def say_hi(self, ctx):
        await ctx.channel.send('Hello ' + ctx.author.name + '!')
```

Now, open up the \_\_init\_\_.py file in the Modules folder and import Greetings.

```python
from .greetings import Greetings
```

Now all that's left is to have the bot load the greetings module. This is done near the bottom of bot.py, by calling load_module before the bot is started.

```python
    bot.load_module('Modules.greetings')
    bot.run()
```

Now run the bot again, and try sending '!hi' in the chat!

### Reacting to Channel Reward Redemptions

Having FoxBot react to a specific reward redemption requires a bit of a workaround, at least until Twitch makes all redemption notifications available either through their API or their IRC interface. Because of this, the reward must be configured to require the user to include text with their redemption.

After the reward is set up with text input required, you will need to find the ID for the reward. Open <https://www.instafluff.tv/TwitchCustomRewardID/?channel=Yourchannel>, but replace 'Yourchannel' in the URL with the name of your channel. Then in another tab, open up your Twitch channel and redeem the reward. Go back to the tab with the Custom Reward ID Finder and copy the reward ID shown. Add it in settings.xml under <custom_rewards>. You can name it whatever you want.

```xml
    <custom_rewards>
        <reward_name>paste reward ID here</reward_name>
    </custom_rewards>
```

In settings.py, you shoould add a method that will return the custom reward ID.

```python
def get_reward_name_id():
    return settings['custom_rewards']['reward_name']
```

Rather than being written as a command, the bot will need to check every incoming message to see if the message context includes your reward's ID. In bot.py, you'll need to add this check to the event_message method, before it checks the message for a valid command.

```python
if 'custom-reward-id' in ctx.tags and ctx.tags['custom-reward-id'] == settings.get_reward_name_id():
    ...
    <whatever you want the bot to do>
    ...
await bot.handle_commands(ctx)
```

<!-- CONTRIBUTING -->
## Contributing

I would love to add more features to this bot. If you've added something, please feel free to contribute it here so others would be able to use it if they like! I only ask that the feature is functional (has been run/tested) prior to submission, and that it doesn't break other existing features.
**Important: Make sure you remove your app_token and client_id before pushing any changes to settings.xml**

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [TwitchCustomRewardID](https://github.com/instafluff/TwitchCustomRewardID)
* [README template](https://github.com/othneildrew/Best-README-Template)
