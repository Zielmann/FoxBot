import xmltodict

def load_settings():
    with open('settings.xml') as f:
        settings = xmltodict.parse(f.read())['settings']
    return settings

settings = load_settings()

def get_app_token():
    return settings['bot_setup']['app_token']

def get_client_id():
    return settings['bot_setup']['client_id']

def get_bot_account():
    return settings['bot_setup']['bot_account']

def get_prefix():
    return settings['bot_setup']['command_prefix']

def get_channel():
    return settings['bot_setup']['channel']

def get_logging():
    return settings['bot_setup']['logging']

def get_twitter():
    return settings['social']['twitter']

def get_discord():
    return settings['social']['discord']

def get_rimworld_mods():
    return settings['games']['rimworld']['mods']

def get_rimworld_events():
    return settings['games']['rimworld']['event_file']

def get_rimworld_items():
    return settings['games']['rimworld']['item_file']

def get_factorio_mods():
    return settings['games']['factorio']['mods']

def get_avorion_link():
    return settings['games']['avorion']['profile_link']

def get_random_tf_id():
    return settings['custom_rewards']['random_tf']

def get_direct_tf_id():
    return settings['custom_rewards']['direct_tf']

