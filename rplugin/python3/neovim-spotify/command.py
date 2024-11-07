from pynvim import Nvim
from typing import Dict

HEIGHT = 48
WIDTH = 3

class Command:
    def __init__(self, nvim: Nvim):
        self.nvim = nvim

    def config_plugin(self) -> None:
        pass
