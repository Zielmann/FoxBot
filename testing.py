import unittest
import twitchio
import bot
import Modules.basics as basics

"""
A set of test cases for the twitchbot, useful for testing offline
and verifying the functionality of new chat commands.

This is a good reference for determining which objects to mock:
https://github.com/TwitchIO/TwitchIO/blob/master/twitchio/dataclasses.py
"""
class TestBotMethods(unittest.TestCase):
    
    def commandCalledTest(self):
        mockctx = unittest.mock.MagicMock(twitchio.Message)
        # Add mock ctx content
        bot.event_ready(mockctx)
        # Assert correct method is called based on ctx

    def correctValueTest(self):
        mockctx = unittest.mock.MagicMock(twitchio.Message)
        # Add mock ctx content (mod here)
        basics.get_shoutout(mockctx)
        # Assert right return value
        