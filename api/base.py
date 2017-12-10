# -*- coding: utf-8 -*-
"""
.. module:: .base.py
    :synopsis: Base API class for dealing with various API's

.. moduleauthor:: Arthur Moore <arthur.moore85@gmail.com>
.. creation date:: 27-10-2017
.. licence:: 
"""
from __future__ import unicode_literals

import os
import urllib
import urllib2

from bs4 import BeautifulSoup
import mechanize

import re
import requests
from requests import ConnectionError

from api.resultset import ResultSet
from io_utils.compression import Compression
from io_utils.platform_io import PlatformBase
from .exceptions import handle_response_codes

__author__ = "arthur"


class Api(object):
    def __init__(self, *args, **kwargs):
        self.service = None
        self.base_url = None
        self.status_code = None
        self.config = None
        self.content = None
        self.current_url = None
        self.response = None
        self.search_regex = None
        self.referrer = None
        self.endpoints = {}
        self.download_url = None
        self.requires_arguments = False
        self.download_arguments = {}
        self.token = None

    def get_response(self):
        """
        Initial request.
        :return: request object.
        """
        if self.current_url:
            url = self.current_url
        else:
            url = self.base_url
        try:
            r = requests.get(url)
        except ConnectionError:
            raise ConnectionError('No internet connection determined.')
        self.status_code = r.status_code

        if self.status_code == 200:
            self.content = r.content
            return r
        else:
            handle_response_codes(self.status_code)

    def _site_request(self, follow=True, data=None):
        url = self.current_url
        extra = dict(cookies=dict(downloadcaptcha='1'))
        if self.referrer is not None:
            extra['headers'] = dict(referer=self.referrer)
        if not follow:
            extra['allow_redirects'] = False
        if data is not None:
            extra['params'] = data
        self.referrer = url
        return requests.get(url, **extra)

    def _get_full_url(self, endpoint):
        """
        Retrieves full URL for a given endpoint if possible.
        Will raise an Exception if no full URL could be found.
        """
        suffix = self.endpoints.get(endpoint)
        if not suffix and suffix != '':
            handle_response_codes('missing_endpoint')
        if not self.base_url:
            handle_response_codes('missing_base_url')
        self.current_url = self.base_url + suffix
        return self.current_url

    def _dictify_search(self, results):
        """
        Returns dictionary/json-like results.
        """
        search_results = {}
        count = 0
        for r in results:
            search_results[count] = {
                'system_id': r[2],
                'system': r[3],
                'game': r[1],
                'url': r[0],
                'filesize': r[4]
            }
            count += 1
        return search_results

    def search(self, query, system=0):
        """
        Searches URL for media.
        :param query: Search query
        :param system: System type
        :return: Dictionary of results.
        """
        search_url = self._get_full_url('search')
        search_results = re.findall(
            self.search_regex,
            self._site_request(
                search_url,
                data=dict(query=query, section='roms', sysid=system)
            ).content
        )
        results = ResultSet(results=search_results, caller=self)
        return results

    def get_download_url(self):
        """
        Returns a download URL.
        :return: URL - string
        """
        f = urllib2.urlopen(self.current_url)
        return f.url

    def download(self, result_item):
        """
        Downloads a ROM.
        :param result_item: ResultItem object.
        """
        self.current_url = result_item.download_url
        location = os.path.join(PlatformBase().download_location, result_item.system_dir)

        # Check if the ROM directory exists, if not, create it.
        if not os.path.exists(location):
            os.makedirs(location)

        req = urllib2.Request(self.base_url)
        req.add_header('Referer', 'https://www.emuparadise.me/')
        self.current_url = self.get_download_url()
        filename = urllib2.unquote(self.current_url.split('/')[-1])
        target_file_name = os.path.join(location, filename)
        urllib.urlretrieve(self.current_url, target_file_name)
        # with open(target_file_name, 'wb') as code:
        #     total_length = f.headers.get('content-length')
        #     if not total_length:
        #         code.write(f.content)
        #     else:
        #         total_length = int(total_length)
        #         while True:
        #             data = f.read(total_length / 100)
        #             if not data:
        #                 break
        #             code.write(data)
        #
        ex = Compression(location)
        ex.extract(target_file_name)