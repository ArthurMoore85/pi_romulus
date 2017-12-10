# -*- coding: utf-8 -*-
"""
.. module:: .platform_io.py
    :synopsis: Platform classes

.. moduleauthor:: Arthur Moore <arthur.moore85@gmail.com>
.. creation date:: 28-10-2017
.. licence::
"""
from __future__ import unicode_literals

import os
import platform

__author__ = "arthur"


class PlatformBase(object):
    """
    This class is intended as an inheritable class.
    It will handle all platform specific tasks.
    """
    def __init__(self):
        self.os = self.get_current_os()
        self.download_location = self._download_directory()

    def get_current_os(self):
        """
        Returns the current Operating System
        :return: OS name (string)
        """
        return platform.system()

    def current_home(self):
        """
        Returns current home directory
        """
        return os.path.expanduser("~")

    def is_retropie(self):
        """
        Checks if this is being ran on a RetroPie.
        :return: Boolean
        """
        pi_path = "/home/pi/RetroPie/roms"
        return os.path.exists(pi_path)

    def _download_directory(self):
        """
        Determines the download location. Windows and Linux only.
        :return: download location (string)
        """
        if self.os == 'Linux':
            if self.is_retropie():
                return '/home/pi/RetroPie/roms'
            else:
                return os.path.join(self.current_home(), 'Downloads', 'roms')
        elif self.os == 'Windows':
            return os.path.join(self.current_home(), 'roms')
