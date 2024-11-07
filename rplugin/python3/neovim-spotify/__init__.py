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

    def config_plugin(self) -> None:

        self.logger.info("Configuring plugin")
        self.nvim.command("hi SpotifyBorder guifg=#1db954")
        self.nvim.command("hi SpotifyText guifg=#1ed760")
        self.nvim.command("hi SpotifySelection guifg=#191414 guibg=#1ed760")

    @pynvim.command("Spotify", sync=True)
    def hello_world(self):
        buf = self.nvim.api.create_buf(False, True)
        print(buf)
        self.nvim.command("echo 'Hello, world!'")
        self.nvim.command(f"echo '{buf.number}'")


