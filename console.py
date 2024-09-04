# -*- coding: utf-8 -*-
# Copyright (C) 2021 github.com/ItsChasa
#
# This source code has been released under the GNU Affero General Public
# License v3.0. A copy of this license is available at
# https://www.gnu.org/licenses/agpl-3.0.en.html
from colorama import Fore

colors = {
    "main_colour": Fore.MAGENTA,
    "light_red": Fore.LIGHTRED_EX,
    "yellow": Fore.YELLOW,
    "light_blue": Fore.LIGHTBLUE_EX,
    "green": Fore.LIGHTGREEN_EX,
    "white": Fore.WHITE,
}

class prnt():
    def __init__(self) -> None:
        pass
    
    def success(self, content, end="\n", indent=0):
        ind = ""
        for _ in range(indent): ind += " "
        print(f"{ind}{colors['green']}>{colors['white']} {content}", end=end)
    
    def info(self, content, end="\n", indent=0):
        ind = ""
        for _ in range(indent): ind += " "
        print(f"{ind}{colors['white']}> {content}", end=end)
    
    def fail(self, content, end="\n", indent=0):
        ind = ""
        for _ in range(indent): ind += " "
        print(f"{ind}{colors['light_red']}>{colors['white']} {content}", end=end)
    
    def inp(self, content, end="\n", indent=0):
        ind = ""
        for _ in range(indent): ind += " "
        print(f"{ind}{colors['light_blue']}>{colors['white']} {content}", end=end)
    
    def warn(self, content, end="\n", indent=0):
        ind = ""
        for _ in range(indent): ind += " "
        print(f"{ind}{colors['yellow']}>{colors['white']} {content}", end=end)