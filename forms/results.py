"""
:module: results.py
:description: Results form

:author: Arthur Moore <arthur.moore85@gmail.com>
:date: 31/12/16
"""
import npyscreen

from api.providers.emuapi import EmuApi
from io_utils.download import Download

__author__ = 'arthur'


class ResultsForm(npyscreen.ActionForm):
    """
    Form that deals with the search results.
    """
    def create(self):
        self.results = self.parentApp.RESULTS
        self.results_box = self.add(npyscreen.BoxTitle, name='Results')
        if self.parentApp.CLEAN_RESULTS:
            self.results_box.values = self.parentApp.CLEAN_RESULTS

    def afterEditing(self):
        selected_option = self.parentApp.SELECTED_RESULT
        try:
            selection = self.parentApp.RESULTS[selected_option]
            self.search = self.parentApp.SCRAPER_OBJ
            self.emu = EmuApi()
            # self.download_link = self.emu.base_url + selection.download_url
            self.emu.download(selection)
            # self.download_link = self.search.get_link(selection)
            npyscreen.notify("Please wait while Romulus downloads this ROM...", "Downloading")
            # self.d = Download()
            # self.d.download(self.download_link, platform=selection.system)
            npyscreen.notify("The ROM is now available on EmulationStation", "Success")
            self.parentApp.setNextForm('MAIN')
        except TypeError:
            npyscreen.notify_wait('Please hit ENTER on your selection to select it', 'Error')

    def on_ok(self):
        self.parentApp.SELECTED_RESULT = self.results_box.value

