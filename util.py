from twitch import TwitchHelix

def validateName(content):
    """
    Returns True if a message's second word is a username starting with @
    """
    valid = False
    if validateNumParameters(content, 2):
        if content.split()[1][0] == '@':
            valid = True
    return valid

def validateNumParameters(content, num):
    """
    Returns True if the content contains the number of parameters indicated by input num
    """
    splitContent = content.split()
    valid = False
    if len(splitContent) == num:
        valid = True
    return valid    

def is_vip(badges):
    """
    Returns True if input contains key 'vip'
    """
    if 'vip' in badges:
        return True
    else:
        return False

# Twitch API call to get stream's game ID. Currently broken.
def checkGame(ctx, client_id, channel, game_name):
    """
    Returns True if the game_name is the Twitch streamer's current game
    """
    if getGameName(ctx, client_id, channel).lower() == game_name.lower():
        return True
    else:
        return False

# Twitch API calls to get stream's current game by name. Currently broken.
def getGameName(ctx, client_id, channel):
    """
    Returns a string containing the current game being played by the streamer
    """
    client = TwitchHelix(client_id)
    stream = client.get_streams(user_logins=channel)._queue[0]
    game_id = stream["game_id"]
    game_info = client.get_games(game_ids=game_id)
    game_name = game_info[0]["name"]
    return game_name
