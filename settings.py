import xmltodict

def load_settings():
    with open('Data/settings.xml') as f:
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

def get_random_tf_id():
    return settings['bot_setup']['custom_rewards']['random_tf']

def get_direct_tf_id():
    return settings['bot_setup']['custom_rewards']['direct_tf']

def get_periodic_messages():
    return settings['bot_setup']['scheduled_messages']['message']

def get_periodic_timer():
    return settings['bot_setup']['scheduled_messages']['message_interval_minutes']

def basics_enabled():
    enable = False
    value = settings['modules']['basics']['enable']
    if value == 'True' or value == 'true':
        enable = True
    return enable

def get_twitter():
    return settings['modules']['basics']['twitter']

def get_discord():
    return settings['modules']['basics']['discord']

def emotes_enabled():
    enable = False
    value = settings['modules']['emotes']['enable']
    if value == 'True' or value == 'true':
        enable = True
    return enable

def get_oof():
    return settings['modules']['emotes']['haurbuOof']

def get_heart():
    return settings['modules']['emotes']['haurbuHeart']

def raffle_enabled():
    enable = False
    value = settings['modules']['raffle']['enable']
    if value == 'True' or value == 'true':
        enable = True
    return enable

def get_raffle_reminder_interval():
    return settings['modules']['raffle']['reminder_interval_minutes']

def quotes_enabled():
    enable = False
    value = settings['modules']['quotes']['enable']
    if value == 'True' or value == 'true':
        enable = True
    return enable

def tf_enabled():
    enable = False
    value = settings['modules']['tf']['enable']
    if value == 'True' or value == 'true':
        enable = True
    return enable

def rimworld_enabled():
    enable = False
    value = settings['modules']['rimworld']['enable']
    if value == 'True' or value == 'true':
        enable = True
    return enable

def get_toolkit_path():
    return settings['modules']['rimworld']['toolkit_path']

def get_rimworld_mods():
    return settings['modules']['rimworld']['mods']

def avorion_enabled():
    enable = False
    value = settings['modules']['avorion']['enable']
    if value == 'True' or value == 'true':
        enable = True
    return enable

def get_avorion_link():
    return settings['modules']['avorion']['profile_link']


