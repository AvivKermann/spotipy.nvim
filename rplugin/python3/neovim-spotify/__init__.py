from pynvim.api.buffer import Buffer
from pynvim.api.nvim import Nvim
from pynvim.api.window import Window
from typing import Dict, Union
import pynvim
import logging


@pynvim.plugin
class NeovimSpotify:
    def __init__(self, nvim: Nvim):
        self.nvim = nvim
        self.buffer: Union[None,Buffer] = None
        self.wins: Dict[Window, bool] = {}
        self.anchor: Union[Window, None] = None
        self.placeholder: Union[None,Buffer] = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    @pynvim.command("Spotify", sync=True)
    def hello_world(self):
        self.nvim.command("echo 'Hello, world!'")
