from twitch import TwitchHelix

# Validates the second parameter starts with @
def validateName(content):
    valid = False
    if validateNumParameters(content, 2):
        if content.split()[1][0] == '@':
            valid = True
    return valid

# Validates the amount of parameters of a ctx context 
def validateNumParameters(content, num):
    splitContent = content.split()
    valid = False
    if len(splitContent) == num:
        valid = True
    return valid    

# Twitch API call to get stream's game ID
def checkGame(ctx, client_id, channel, game_name):
    if getGameName(ctx,client_id,channel).lower() == game_name.lower():
        return True
    else:
        return False

# Twitch API calls to get stream's current game by name
def getGameName(ctx,client_id,channel):
    client = TwitchHelix(client_id)
    stream = client.get_streams(user_logins=channel)._queue[0]
    game_id = stream["game_id"]
    game_info = client.get_games(game_ids=game_id)
    game_name = game_info[0]["name"]
    return game_name
