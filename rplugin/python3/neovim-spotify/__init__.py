from pynvim.api.nvim import Nvim
import pynvim
import time
from .plugin import Plugin
from .spotify import Track

@pynvim.plugin
class NeovimSpotify:
    def __init__(self, nvim: Nvim):
        self.plugin = Plugin(nvim)

    @pynvim.function("SpotifyLine", sync=False)
    def spotify(self, _):
        self.plugin.nvim.vars["spotify_line"] = self.plugin.get_track_status()

    @pynvim.command("SpotifyToggle", sync=True)
    def spotify_toggle(self):
        device_id = self.plugin.nvim.vars.get("spotify_device", None)
        if device_id:
            device_id = device_id["id"]
        playback = self.plugin.spotify.spotify.current_playback()
        if not playback and not device_id:
            status_message = ("No device found.\n"
                              "Use :SpotifyDevices to select a device\n"
                              )
            cmd = f"vim.notify({repr(status_message)}, vim.log.levels.INFO, {{title = 'Spotify'}})"
            self.plugin.nvim.exec_lua(cmd)
            return

        self.plugin.spotify.toggle(playback=playback, device_id=device_id)
        time.sleep(0.5)
        self.spotify_status()


    @pynvim.command("SpotifyPlayback", nargs=1, sync=True)
    def spotify_playback(self, args: str = ""):
        args = args[0].strip().lower() if args else ""
        if args in ["-n", "next"]:
            self.plugin.spotify.next()
            self.spotify_status()
            return
        elif args in ["-p", "prev"]:
            self.plugin.spotify.prev()
            self.spotify_status()
            return

        else:
            self.plugin.nvim.command("echo 'Invalid argument. Use -n or next for next song, or -p or prev for previous song.'")
            return

    @pynvim.command("SpotifySearch", nargs="*", sync=False)
    def spotify_search(self, args) -> None:
        if not args or not args[0]:
            self.plugin.nvim.command("echo 'Must provide a search query while using search command'")
            return
        tracks = self.plugin.search(" ".join(args))
        self.plugin.nvim.vars["spotify_results"] = tracks
        self.plugin.nvim.vars["spotify_query"] = " ".join(args)
        self.plugin.nvim.exec_lua("require('neovim-spotify').init()")
        
    @pynvim.command("SpotifyPlay", nargs=1, sync=False)
    def spotify_play(self, args: str):
        if not args or not args[0]:
            self.plugin.nvim.command("echo 'Must provide a track uri'")
            return
        device_id = self.plugin.nvim.vars.get("spotify_device", None)
        if device_id:
            device_id = device_id["id"]
        self.plugin.spotify.play(" ".join(args), device_id)
        time.sleep(0.5)
        self.spotify_status()

    @pynvim.command("SpotifyStatus", sync=False)
    def spotify_status(self):
        status_message = self.plugin.get_current_status()
        if not status_message:
            status_message = ("No track is currently playing!\n"
                              "Use :SpotifySearch to search for a track\n"
                             )

        cmd = f"vim.notify({repr(status_message)}, vim.log.levels.INFO, {{title = 'Spotify'}})"
        self.plugin.nvim.exec_lua(cmd)

    @pynvim.command("SpotifyPlaylist", nargs=0, sync=False)
    def spotify_playlist(self):
        playlist = self.plugin.spotify.get_playlist()
        if playlist is None:
            return


        self.plugin.nvim.vars["spotify_results"] = playlist
        self.plugin.nvim.vars["spotify_query"] = "Current Queue"
        self.plugin.nvim.exec_lua("require('neovim-spotify').init()")


    @pynvim.command("SpotifyDevices", nargs=0, sync=False)
    def spotify_devices(self) -> None:
        devices = self.plugin.spotify.get_devices()
        self.plugin.nvim.vars["spotify_devices"] = devices
        self.plugin.nvim.exec_lua("require('neovim-spotify').show_devices()")

    @pynvim.command("SpotifyAdd", nargs=1, sync=False)
    def spotify_add(self, args: str) -> None:
        if not args or not args[0]:
            self.plugin.nvim.command("echo 'Must provide a track'")

        device_id = self.plugin.nvim.vars.get("spotify_device", "")
        self.plugin.spotify.add_to_queue(" ".join(args), device_id)

