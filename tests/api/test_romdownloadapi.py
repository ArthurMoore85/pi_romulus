"""
..module: .test_romdownloadapi.py
..description: Unittests for RomDownload API

..author: Arthur Moore <arthur.moore85@gmail.com>
..date: 2021-02-07
"""
from __future__ import unicode_literals

import unittest

from api.providers.romsdownload import RomsDownloadApi


class RomDownloadApiTestCase(unittest.TestCase):
    """
    TestCase for the RomDownloadAPI.
    """
    def setUp(self):
        self.rd = RomsDownloadApi()

    def test_convert_to_download_link(self):
        """
        Tests the convert_to_download_link method.

        Expected: returns download_link and
        download_id.
        """
        expected_link = 'https://romsdownload.net/download/roms/snes/super-mario-1234'
        expectd_id = '1234'
        link = 'http://test/games/snes/super-mario-1234'
        dl, did = self.rd.convert_to_download_link(
            link
        )
        self.assertEquals(
            dl, expected_link
        )
        self.assertEquals(
            did, expectd_id
        )
