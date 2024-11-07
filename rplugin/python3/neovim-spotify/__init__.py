from command import Command
import pynvim

@pynvim.plugin
class NeovimSpotify:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command("Spotify", sync=True)
    def hello_world(self):
        self.nvim.command("echo 'Hello, world!'")
