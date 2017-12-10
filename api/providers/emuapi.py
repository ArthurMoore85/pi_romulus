# -*- coding: utf-8 -*-
"""
.. module:: .emuapi.py
    :synopsis: EmuParadise API

.. moduleauthor:: Arthur Moore <arthur.moore85@gmail.com>
.. creation date:: 27-10-2017
.. licence:: 
"""
from __future__ import unicode_literals

import HTMLParser
import urllib2

import requests

from api.base import Api

__author__ = "arthur"

ENDPOINTS = {
    'search': '/roms/search.php'
}


class EmuApi(Api):
    """
    EmuParadise API.
    This provides an easy to use API to connect to EmuParadise,
    and extract information and data from the website.
    """
    def __init__(self):
        super(EmuApi, self).__init__()
        self.service = 'EmuParadise'
        self.base_url = 'https://www.emuparadise.me'
        self.referrer = None
        self._parser = HTMLParser.HTMLParser()
        self.endpoints = ENDPOINTS
        self.response = self.get_response()
        self.search_regex = '<div class="roms">' \
                            '<a .*?href="(.*?)">(.*?)</a>.*?' \
                            '<a href="\/roms\/roms\.php\?sysid=(\d+)".*?class="sysname">' \
                            '(.*?)</a>.*?<b>Size:</b> (.*?) .*?</div>'
        self.download_url = 'http://direct.emuparadise.me/roms/get-download.php?gid={download_id}' \
                            '&token={token}' \
                            '&mirror_available=true'
        self.requires_arguments = True
        self.token = '211217baa2d87c57b360b9a673a12cfd'

    def get_download_url(self):
        """
        Overwrites the get_download_url method to run validation checks.
        """
        url = super(EmuApi, self).get_download_url()

        # Validate the URL.
        # EmuParadise will (when token expired etc) redirect the user back
        # to the original details page. This has a URL ending in the game ID.
        # However, when the link is a valid DL link, it ends in the filename.
        # To validate the link, we can check if the ending can be converted to
        # an int. If it can, we know thats the game ID and thus invalid.
        try:
            int(url.split('/')[-1])
        except ValueError:
            return url
        else:
            # Its an invalid URL, first lets turn the URL into the link
            url += '-download'
            r = requests.get(url)
            data = r.text
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(data)
            link = self.base_url + soup.find('a', {'id': 'download-link'}).get('href')
            req = urllib2.Request(link)
            req.add_header('Referer', 'https://www.emuparadise.me/')
            f = urllib2.urlopen(req)
            self.current_url = f.url
            return f.url
