from .plugin import Plugin
from pynvim.api.nvim import Nvim
import pynvim

@pynvim.plugin
class NeovimSpotify:
    def __init__(self, nvim: Nvim):
        self.plugin = Plugin(nvim)

    @pynvim.command("Spotify", sync=True)
    def hello_world(self):

        # this works for sure to create a buffer.
        buf = self.plugin.nvim.api.create_buf(False, True)
        self.plugin.get_currently_playing_track()



