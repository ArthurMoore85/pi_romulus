"""
..module: .filter.py
..description: Form to filter by system

..author: Arthur Moore <arthur.moore85@gmail.com>
..date: 2021-02-07
"""
import sys
import npyscreen as npyscreen

from forms import SearchForm

class FilterForm(npyscreen.FormMultiPageAction):
    """
    This form presents the user with a form whereby they can select
    what systems to show results for.
    """
    def _get_filtered_systems(self):
        """
        Returns a list of the systems to filter on.
        """
        filtered = []
        show_all = False
        if self.all_box.value:
            show_all = True
        else:
            selected_systems = {
                'Amstrad CPC': self.amstrad_box.value,
                'Atari 2600': self.atari26_box.value,
                'Atari 7800': self.atari78_box.value,
                'Atari Lynx': self.lynx_box.value,
                'MAME': self.mame_box.value,
                'Neo Geo': self.neo_box.value,
                'Neo Geo Pocket Color': self.neo_pocket_box.value,
                'Nintendo 64': self.n64_box.value,
                'Nintendo': self.nes_box.value,
                'Nintendo Famicom Disk System': self.nes_disc_box.value,
                'Gameboy': self.gb_box.value,
                'Gameboy Color': self.gbc_box.value,
                'Gameboy Advance': self.gba_box.value,
                'TurboGrafx 16': self.turbo_box.value,
                'Playstation Portable': self.psp_box.value,
                'Sega 32X': self.s32x_box.value,
                'Sega CD': self.scd_box.value,
                'Game Gear': self.gg_box.value,
                'Sega Genesis': self.genesis_box.value,
                'Sega Master System': self.master_box.value,
                'Sony Playstation': self.ps_box.value,
                'Super Nintendo': self.snes_box.value,
                'ZX Spectrum': self.spec_box.value,
                'Sega Dreamcast': self.dream_box.value,
                'Nintendo DS': self.ds_box.value,
                'ScummVM': self.scumm_box.value
            }
            for system, value in selected_systems.items():
                if value:
                    filtered.append(system)

        return filtered, show_all        

    def create(self):
        """
        Creates form upon initialization by main app.
        """
        self.rom = self.add(npyscreen.TitleText, name='Select system to search on: ')
        self.all_box = self.add(npyscreen.CheckBox, name='Show for all systems')
        self.amstrad_box = self.add(npyscreen.CheckBox, name='Amstrad CPC')
        self.atari26_box = self.add(npyscreen.CheckBox, name='Atari 2600')
        self.atari78_box = self.add(npyscreen.CheckBox, name='Atari 7800')
        self.lynx_box = self.add(npyscreen.CheckBox, name='Atari Lynx')
        self.mame_box = self.add(npyscreen.CheckBox, name='MAME')
        self.neo_box = self.add(npyscreen.CheckBox, name='Neo Geo')
        self.neo_pocket_box = self.add(npyscreen.CheckBox, name='Neo Geo Pocket Color')
        self.n64_box = self.add(npyscreen.CheckBox, name='Nintendo 64')
        self.nes_box = self.add(npyscreen.CheckBox, name='Nintendo Entertainment System / NES')
        self.nes_disc_box = self.add(npyscreen.CheckBox, name='Famicom Disk System')
        self.gb_box = self.add(npyscreen.CheckBox, name='Gameboy')
        self.gbc_box = self.add(npyscreen.CheckBox, name='Gameboy Color')
        self.gba_box = self.add(npyscreen.CheckBox, name='Gameboy Advance')
        self.turbo_box = self.add(npyscreen.CheckBox, name='Turbografx 16')
        self.psp_box = self.add(npyscreen.CheckBox, name='Playstation Portable / PSP')
        self.s32x_box = self.add(npyscreen.CheckBox, name='Sega 32X')
        self.scd_box = self.add(npyscreen.CheckBox, name='Sega CD')
        self.add_page()
        self.gg_box = self.add(npyscreen.CheckBox, name='Sega GameGear')
        self.genesis_box = self.add(npyscreen.CheckBox, name='Sega Genesis/MegaDrive')
        self.master_box = self.add(npyscreen.CheckBox, name='Sega Master System')
        self.ps_box = self.add(npyscreen.CheckBox, name='Sony PlayStation')
        self.snes_box = self.add(npyscreen.CheckBox, name='Super Nintendo / SNES')
        self.spec_box = self.add(npyscreen.CheckBox, name='ZX Spectrum')
        self.dream_box = self.add(npyscreen.CheckBox, name='Sega Dreamcast')
        self.ds_box = self.add(npyscreen.CheckBox, name='Nintendo DS')
        self.scumm_box = self.add(npyscreen.CheckBox, name='SCUMMVM')

    def on_ok(self):
        """
        Carried out when OK button is pressed
        """
        # npyscreen.notify("Please wait", "Searching...")
        # self.romsdownload = RomsDownloadApi()
        # self.search = self.romsdownload.search(self.rom.value)
        # # self.search = Scraper(self.rom.value, parent=self)
        # self.results = clean_results_list(self.search)
        # self.clean_results = self.results[0]
        # self.parentApp.SCRAPER_OBJ = self.search
        # self.parentApp.CLEAN_RESULTS = self.clean_results
        # self.parentApp.RESULTS = self.results[1]
        self.parentApp.FILTERED_SYSTEMS, self.parentApp.SHOW_ALL = self._get_filtered_systems()

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
        self.parentApp.addForm('SEARCH', SearchForm, name="Search")
        self.parentApp.setNextForm('SEARCH')
