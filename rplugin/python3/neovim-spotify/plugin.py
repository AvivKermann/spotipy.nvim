from pynvim.api.buffer import Buffer
from pynvim.api.nvim import Nvim
from pynvim.api.window import Window
from typing import Dict, Union
from .spotify import Spotify, Track
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



    def get_currently_playing_track(self) -> Track:
        self.logger.info("Getting currently playing track")
        return self.spotify.get_currently_playing_track()


    def search(self, query: str, search_type: str = "track"):
        self.logger.info(f"Searching for track: {query}")
        tracks = self.spotify.search(query=query, search_type=search_type)
        return tracks

