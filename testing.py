import unittest
import unittest.mock as mock
import twitchio
import Modules

"""
A set of test cases for the twitchbot, useful for testing offline
and verifying the functionality of new chat commands.

This is a good reference for determining which objects to mock:
https://github.com/TwitchIO/TwitchIO/blob/master/twitchio/dataclasses.py
"""

class TestBasicsMethods(unittest.TestCase):
    # Need to make the test bot utilize a temporary settings file

    def test_correctShoutout(self):
        """
        Test that the correct output is created for the chat message content
        """
        correctResponse = 'Shoutout to testuser! Check out their stream at twitch.tv/testuser and give them a follow!'

        mockctx = mock.MagicMock(twitchio.Message)
        mockctx.author.is_mod = True
        mockctx.content = '!shoutout @testuser'

        response = Modules.basics.get_shoutout(mockctx)
        self.assertEqual(response, correctResponse)