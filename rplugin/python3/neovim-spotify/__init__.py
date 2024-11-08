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

    @pynvim.command("SpotifyToggle", sync=True)
    def spotify_toggle(self):
        self.plugin.spotify.toggle()


    @pynvim.command("SpotifyPlayback", nargs=1, sync=True)
    def spotify_playback(self, args: str = ""):
        self.plugin.nvim.out_write(f"args: {args}\n")
        args = args.strip().lower() if args else ""
        if args in ["-n", "next"]:
            self.plugin.spotify.next()
            return
        elif args in ["-p", "prev"]:
            self.plugin.spotify.prev()
            return
        else:
            self.plugin.nvim.command("echo 'Invalid argument. Use -n or next for next song, or -p or prev for previous song.'")
            return

    


