from pynvim.api.nvim import Nvim
import pynvim
import time
from .plugin import Plugin

@pynvim.plugin
class NeovimSpotify:
    def __init__(self, nvim: Nvim):
        self.plugin = Plugin(nvim)

    @pynvim.command("SpotifyLine", sync=True)
    def spotify(self):
        self.plugin.nvim.vars["spotify_line"] = repr(self.plugin.get_track_status())
        return self.plugin.get_track_status()

    @pynvim.command("SpotifyToggle", sync=True)
    def spotify_toggle(self):
        self.plugin.spotify.toggle()
        self.spotify_status()


    @pynvim.command("SpotifyPlayback", nargs=1, sync=True)
    def spotify_playback(self, args: str = ""):
        args = args[0].strip().lower() if args else ""
        if args in ["-n", "next"]:
            self.plugin.spotify.next()
            time.sleep(0.5)
            self.spotify_status()
            return
        elif args in ["-p", "prev"]:
            self.plugin.spotify.prev()
            time.sleep(0.5)
            self.spotify_status()
            return

        else:
            self.plugin.nvim.command("echo 'Invalid argument. Use -n or next for next song, or -p or prev for previous song.'")
            return

    @pynvim.command("SpotifySearch", nargs="*", sync=True)
    def spotify_search(self, args) -> None:
        if not args or not args[0]:
            self.plugin.nvim.command("echo 'Must provide a search query while using search command'")
            return
        tracks = self.plugin.search(" ".join(args))
        self.plugin.nvim.vars["spotify_search_results"] = tracks
        self.plugin.nvim.vars["spotify_search_query"] = " ".join(args)
        self.plugin.nvim.exec_lua("require('neovim-spotify').init()")
        
    @pynvim.command("SpotifyPlay", nargs=1, sync=True)
    def spotify_play(self, args: str):
        if not args or not args[0]:
            self.plugin.nvim.command("echo 'Must provide a track uri'")
            return
        self.plugin.spotify.play(" ".join(args))
        time.sleep(0.5)
        self.spotify_status()

    @pynvim.command("SpotifyStatus", sync=True)
    def spotify_status(self):
        track = self.plugin.spotify.get_currently_playing_track()
        if track.exists:
            progress = track.get_progress()
            duration = track.get_duration()
            status_message = (
                f"Song: {track.title}\n"
                f"Artist: {track.artist}\n"
                f"Progress: {progress}/{duration}"
            )
            lua_code = f"""
            vim.notify("{repr(status_message)[1:-1]}", vim.log.levels.INFO, {{title = "Spotify"}})
            """
            self.plugin.nvim.command('lua ' + lua_code)


