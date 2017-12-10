# -*- coding: utf-8 -*-
"""
.. module:: .emuapi.py
    :synopsis: Unittests for the EmuParadise API wrapper and base Api.

.. moduleauthor:: Arthur Moore <arthur.moore85@gmail.com>
.. creation date:: 04-11-2017
.. licence:: 
"""
from __future__ import unicode_literals

import unittest

from api.providers import EmuApi
from api.resultset import ResultSet

__author__ = "arthur"


class EmuApiTest(unittest.TestCase):
    """
    TestCase for the EmuApi class.
    """
    def setUp(self):
        self.emu = EmuApi()

    def test_get_response(self):
        """
        Tests the base class get_response method.
        """
        self.assertTrue(
            self.emu.get_response().status_code,
            200
        )
        self.assertTrue(self.emu.status_code, 200)

    def test_search(self):
        """
        Tests the base class search method.
        """
        search_response = self.emu.search('Sonic Pinball')
        self.assertEquals(type(search_response), ResultSet)
