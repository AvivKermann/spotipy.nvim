from pynvim import Nvim, Buffer, Window
from typing import Dict

HEIGHT = 48
WIDTH = 3

class Command:
    def __init__(self, nvim: Nvim):
        self.nvim = nvim
        self.buffer = Buffer
        self.windows: Dict[Window, bool] = {}
        self.anchor: Window = None 
        self.placeholder: Buffer = None

    def config_plugin(self) -> None:
        pass
