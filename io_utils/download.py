"""
:module: download.py
:description: Downloading module

:author: Arthur Moore <arthur.moore85@gmail.com>
:date: 31/12/16
"""
import os
import urllib
import urllib2

from scraping.scraper import Scraper
from .directory_utils import Directories
from .platform_io import PlatformBase

__author__ = 'arthur'


class Download(PlatformBase):
    """
    Downloads a ROM/Game
    """
    def __init__(self, *args, **kwargs):
        super(Download, self).__init__()
        self.url = None
        self.dirs_obj = Directories()
        self.search = Scraper()

    # def download(self, link, platform):
    #     """
    #     Downloads the ROM
    #     """
    #     # platform = " ".join(rom_url.split('/')[3].replace('_', ' ').split()[:-1])
    #     target = self.dirs_obj.target_directory(self.download_location, platform)
    #
    #     req = urllib2.Request(link)
    #     req.add_header('Referer', 'https://www.emuparadise.me/')
    #     file_name = urllib2.unquote(link.split('/')[-1])
    #     target_file_name = os.path.join(target, file_name)
    #     urllib.urlretrieve(link, target_file_name)
    #     f = urllib2.urlopen(link)
    #     with open(target_file_name, 'wb') as code:
    #         total_length = f.headers.get('content-length')
    #         if not total_length:
    #             code.write(f.content)
    #         else:
    #             total_length = int(total_length)
    #             while True:
    #                 data = f.read(total_length / 100)
    #                 if not data:
    #                     break
    #                 code.write(data)
    #
    #     ex = Compression(location)
    #     ex.extract(target_file_name)
