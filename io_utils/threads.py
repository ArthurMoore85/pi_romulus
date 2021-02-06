# -*- coding: utf-8 -*-
"""
.. module:: .threads.py
    :synopsis: Handles threading.

.. moduleauthor:: Arthur Moore <arthur.moore85@gmail.com>
.. creation date:: 21-05-2018
.. licence:: 
"""
from __future__ import unicode_literals

import threading

from api.providers.emuapi import EmuApi
from api.providers.romsdownload import RomsDownloadApi

__author__ = "arthur"


class ThreadDownload(threading.Thread):
    """
    Downloads the ROM in a new thread,
    """

    def __init__(self, selection):
        threading.Thread.__init__(self)
        self.selection = selection

    def run(self):
        """
        Start the download thread.
        """
        if self.selection:
            self.emu = RomsDownloadApi()
            self.emu.download(self.selection)
