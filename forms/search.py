"""
:module: search.py
:description: Search form

:author: Arthur Moore <arthur.moore85@gmail.com>
:date: 31/12/16
"""
import sys

import npyscreen as npyscreen

from api.providers import EmuApi
from forms.results import ResultsForm

__author__ = 'arthur'


def clean_results_list(results):
    """
    Returns a clean list of results
    """
    results_list = []
    results_dict = {}
    count = 0
    for rom in results.all():
        display = '{0} - {1}'.format(rom.name, rom.system)
        results_dict[count] = rom
        results_list.append(display)
        count += 1
    return results_list, results_dict


class SearchForm(npyscreen.ActionForm):
    """
    This form presents the user with a search form from where they can search for a
    ROM or other game from EmuParadise.
    """
    def create(self):
        """
        Creates form upon initialization by main app.
        """
        self.rom = self.add(npyscreen.TitleText, name='Game: ')

    def on_ok(self):
        """
        Carried out when OK button is pressed
        """
        npyscreen.notify("Please wait", "Searching...")
        self.emu = EmuApi()
        self.search = self.emu.search(self.rom.value)
        # self.search = Scraper(self.rom.value, parent=self)
        self.results = clean_results_list(self.search)
        self.clean_results = self.results[0]
        self.parentApp.SCRAPER_OBJ = self.search
        self.parentApp.CLEAN_RESULTS = self.clean_results
        self.parentApp.RESULTS = self.results[1]

    def on_cancel(self):
        """
        Carried out when Cancel button is pressed
        """
        sys.exit()

    def afterEditing(self):
        """
        Everything here is ran after on_ok is completed.
        Note that all forms added in the parentApp are loaded with their data before
        the app formally begins. Therefore the Results form is declared here to ensure
        that the results data is loaded AFTER we have the results. Declaring the results form
        in the parentApp would load the form without the results.
        """
        self.parentApp.addForm('RESULTS', ResultsForm, name="Results")
        self.parentApp.setNextForm('RESULTS')
