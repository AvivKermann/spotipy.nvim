from pynvim.api.buffer import Buffer
from pynvim.api.nvim import Nvim
from pynvim.api.window import Window
from typing import Dict, Union
from .ui import  create_anchor, create_placeholder
from .actions import fetch_currently_playing_track, create_input
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


    def start(self) -> None:
        self.config_plugin()

        create_placeholder(self)
        fetch_currently_playing_track(self)
        create_input(self)

    def config_plugin(self) -> None:

        self.logger.info("Configuring plugin")
        self.nvim.command("hi SpotifyBorder guifg=#1db954")
        self.nvim.command("hi SpotifyText guifg=#1ed760")
        self.nvim.command("hi SpotifySelection guifg=#191414 guibg=#1ed760")
        create_anchor(self)

    @pynvim.command("Spotify", sync=True)
    def hello_world(self):
        self.nvim.command("echo 'Hello, world!'")


