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

from bs4 import BeautifulSoup

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

    def fetch_webpage(self, url):
        """
        Fetches the data from a webpage and returns a BeautifulSoup
        object.
        :param url: URL to fetch
        :return: BeautifulSoup data
        """
        r = requests.get(url)
        data = r.text
        return BeautifulSoup(data)

    def get_next_url(self, page):
        """
        Retrieves the next URL data leading towards the
        download URL.
        :param page: last page object.
        :return:
        """
        download_div = page.find('div', {'class': 'download-link'})
        new_url = 'https://direct.emuparadise.me' + download_div.find('a').get('href')
        return new_url

    def verify_link(self, page):
        """
        Verifies that the link is the download link.
        :return: Boolean
        """
        return True if page.find('a', {'id': 'download-link'}) else False

    def get_direct_url(self, page):
        """
        Returns the direct download link
        :param page: Page to search for link.
        :return: String
        """
        url_list = page.find_all('a', {'id': 'download-link'})
        if url_list:
            return url_list[0]
        else:
            return None

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
            new_url = url + '-download'
            page = self.fetch_webpage(new_url)
            is_final_page = self.verify_link(page)
            while not is_final_page:
                url = self.get_next_url(page)
                page = self.fetch_webpage(url)
                is_final_page = self.verify_link(page)

            direct_link = self.get_direct_url(page)

            link = self.base_url + direct_link.get('href')
            req = urllib2.Request(link)
            req.add_header('Referer', 'https://www.emuparadise.me/')
            f = urllib2.urlopen(req)
            self.current_url = f.url
            return f.url
