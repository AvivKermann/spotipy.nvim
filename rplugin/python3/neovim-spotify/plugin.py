from pynvim.api.buffer import Buffer
from pynvim.api.nvim import Nvim
from pynvim.api.window import Window
from typing import Dict, Union
from .spotify import Spotify
import logging

class Plugin:
    WIDTH = 48
    HEIGHT = 3
    def __init__(self, nvim: Nvim):
        self.nvim = nvim
        self.buffer: Union[None,Buffer] = None
        self.wins: Dict[Window, bool] = {}
        self.anchor: Union[Window, None] = None
        self.placeholder: Union[None,Buffer] = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.spotify = Spotify()



    def get_currently_playing_track(self):
        self.logger.info("Getting currently playing track")
        track = self.spotify.get_currently_playing_track()
        self.nvim.out_write(f"Currently playing: {track}\n")

    def search(self, query: str, search_type: str = "track"):
        self.logger.info(f"Searching for track: {query}")
        tracks = self.spotify.search(query=query, search_type=search_type)
        self.nvim.vars["spotify_search_results"] = tracks
        self.nvim.exec_lua("require('neovim-spotify').init()")

