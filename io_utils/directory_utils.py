"""
:module: directory_utils.py
:description: Deals with directories and their creation

:author: Arthur Moore <arthur.moore85@gmail.com>
:date: 26/11/16
"""
import os

__author__ = 'arthur'


SYSTEMS = {
    'Amstrad CPC': 'amstradcpc', 'Atari 2600': 'atari2600', 'Atari 7800': 'atari7800', 'Atari Lynx': 'atarilynx',
    'M.A.M.E. - Multiple Arcade Machine Emulator': 'mame-libretro',
    'Neo Geo': 'neogeo', 'Neo Geo Pocket - Neo Geo Pocket Color': 'ngp', 'Nintendo 64': 'n64',
    'Nintendo Entertainment System': 'nes', 'Nintendo Famicom Disk System': 'fds', 'Nintendo Game Boy': 'gb',
    'Nintendo Game Boy Color': 'gbc', 'Nintendo Gameboy Advance': 'gba', 'PC Engine - TurboGrafx16': 'pcengine',
    'PSP': 'psp', 'Sega 32X': 'sega32x', 'Sega CD': 'segacd', 'Sega Game Gear': 'gamegear',
    'Sega Genesis - Sega Megadrive': 'megadrive', 'Sega Master System': 'mastersystem', 'Sony Playstation': 'psx',
    'Super Nintendo Entertainment System': 'snes', 'ZX Spectrum': 'zxspectrum'
}


class Directories(object):
    """
    Directories object
    """
    def target_directory(self, base_dir, game_category):
        sub_dir = SYSTEMS[game_category]
        full_dir = os.path.join(base_dir, sub_dir)
        if not os.path.exists(full_dir):
            os.makedirs(full_dir)
        return full_dir
