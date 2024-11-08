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
        args = args[0].strip().lower() if args else ""
        if args in ["-n", "next"]:
            self.plugin.spotify.next()
            return
        elif args in ["-p", "prev"]:
            self.plugin.spotify.prev()
            return
        else:
            self.plugin.nvim.command("echo 'Invalid argument. Use -n or next for next song, or -p or prev for previous song.'")
            return

    @pynvim.command("SpotifySearch", nargs="*", sync=True)
    def spotify_search(self, args):
        if not args or not args[0]:
            return []

        search_query = args[0]
        tracks = self.plugin.spotify.search(search_query, search_type="track")
        self.plugin.nvim.out_write(f"Tracks: {tracks}")
        return tracks        

        


    


