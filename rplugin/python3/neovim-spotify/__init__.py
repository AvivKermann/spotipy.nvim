from pynvim.api.buffer import Buffer
from pynvim.api.nvim import Nvim
from pynvim.api.window import Window
from typing import Dict, Union
import pynvim
import logging
import subprocess

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

        # this works for sure to create a buffer.
        buf = self.nvim.api.create_buf(False, True)
        get_currently_playing_track(self)



def get_currently_playing_track(self):
    self.logger.info("Getting currently playing track")
    response = subprocess.run("spt playback -s -f '%t by %a'", shell=True, capture_output=True)
    if response.returncode != 0:
        self.logger.error("Error getting currently playing track")
        return
    self.nvim.command("echo '{response.stdout.decode().split()}'")
