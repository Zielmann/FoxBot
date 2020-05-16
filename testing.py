import unittest
import twitchio
import bot
import Modules

"""
A set of test cases for the twitchbot, useful for testing offline
and verifying the functionality of new chat commands.

This is a good reference for determining which objects to mock:
https://github.com/TwitchIO/TwitchIO/blob/master/twitchio/dataclasses.py
"""
class TestBotMethods(unittest.TestCase):
    
    # Need to make the test bot utilize a temporary settings file
    def commandCalledTest(self):
        """
        Test that the correct method is called upon the correct chat message
        """
        mockctx = unittest.mock.MagicMock(twitchio.Message)
        mockctx.content = unittest.mock.Mock(return_value='@Haurbus')
        bot.event_message(mockctx)
        #Modules.basics.get_bot_info()
        self.assertEqual(True, True)

    def correctValueTest(self):
        """
        Test that the correct output is created for the chat message content
        """
        mockctx = unittest.mock.MagicMock(twitchio.Message)
        # Add mock ctx content (mod here)
        Modules.basics.get_shoutout(mockctx)
        # Assert right return value
        