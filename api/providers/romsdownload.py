"""
..module: .roms_games.py
..description: Roms Downloads API

..author: Arthur Moore <arthur.moore85@gmail.com>
"""
from __future__ import unicode_literals

import os
import re
import HTMLParser
import urllib
import urllib2

import requests

from bs4 import BeautifulSoup

from api.resultset import ResultSet

from api.base import Api
from io_utils.platform_io import PlatformBase
from io_utils.compression import Compression

__author__ = "arthur"

ENDPOINTS = {
    'search': '/roms/search.php'
}


class RomsDownloadApi(Api):
    """
    RomsDownload API.
    This provides an easy to use API to connect to RomsDownload,
    and extract information and data from the website.
    """

    def __init__(self):
        super(RomsDownloadApi, self).__init__()
        self.service = 'RomsDownload'
        self.base_url = 'https://romsdownload.net'
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

    def convert_to_download_link(self, link):
        """
        Injects the game link with string to turn it into a direct
        download link.
        """
        link_system, link_game = link.split('/')[4:]
        download_id = link_game.split('-')[-1]
        download_link = '{root}/download/roms/{system}/{game}'.format(
            root=self.base_url,
            system=link_system,
            game=link_game
        )

        return download_link, download_id

    def extract_table(self, bs_obj):
        """
        Extracts all the relevant data from the table.
        """
        table_rows = bs_obj.findAll('table')[0].find_all('tr')[1:]
        games = {}
        counter = 0
        for row in table_rows:
            data = row.find_all('td')
            game_name = data[0].text.strip()
            game_link, download_id = self.convert_to_download_link(
                data[0].find_all('a', href=True)[0]['href'])
            system_name = data[1].text.strip()
            rating = data[2].text.strip()
            downloads = data[3].text.strip()
            games[counter] = {
                'download_id': download_id,
                'game_name': game_name,
                'game_link': game_link,
                'system_name': system_name,
                'rating': rating,
                'downloads': downloads
            }
            counter += 1

        return games

    def search(self, query, system=0):
        """
        Overrides the search method to list the games available.
        """
        query = "+".join(query.split())
        search_url = "https://romsdownload.net/search?name={query}".format(
            query=query)
        returns = requests.get(search_url).content
        # search_results = re.findall(
        #     self.search_regex,
        #     self._site_request(
        #         search_url,
        #         data=dict(query=query, section='roms', sysid=system)
        #     ).content
        # )
        bs = BeautifulSoup(returns, "html.parser")
        search_results = self.extract_table(bs)
        results = ResultSet(results=search_results, caller=self)

        return results

    def fetch_webpage(self, url):
        """
        Fetches the data from a webpage and returns a BeautifulSoup
        object.
        :param url: URL to fetch
        :return: BeautifulSoup data
        """
        r = requests.get(url)
        data = r.text
        return BeautifulSoup(data, 'html.parser')

    def get_next_url(self, page):
        """
        Retrieves the next URL data leading towards the
        download URL.
        :param page: last page object.
        :return:
        """
        download_div = page.find('div', {'class': 'download-link'})
        new_url = 'https://direct.emuparadise.me' + \
            download_div.find('a').get('href')
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

    def download(self, result_item):
        """
        Overwrites the download method to handle downloads
        from RomsDownload.
        """
        self.current_url = result_item.download_url
        bs = BeautifulSoup(requests.get(
            self.current_url).content, 'html.parser')
        location = os.path.join(
            PlatformBase().download_location, result_item.system_dir)

        # Check if the ROM directory exists, if not, create it.
        if not os.path.exists(location):
            os.makedirs(location)

        req = urllib2.Request(self.base_url)
        req.add_header('Referer', 'https://www.emuparadise.me/')
        self.current_url = bs.findAll('a', {'class': 'wait__link'})[0]['href']
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
