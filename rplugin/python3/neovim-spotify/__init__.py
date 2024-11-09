from .plugin import Plugin
from pynvim.api.nvim import Nvim
import pynvim
from typing import Any

@pynvim.plugin
class NeovimSpotify:
    def __init__(self, nvim: Nvim):
        self.plugin = Plugin(nvim)

    @pynvim.command("Spotify", sync=True)
    def spotify(self):

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
    def spotify_search(self, args) -> Any:
        if not args or not args[0]:
            self.plugin.nvim.command("echo 'Must provide a search query while using search command'")
            return []
        tracks = self.plugin.search(" ".join(args))
        self.plugin.nvim.vars["spotify_search_results"] = tracks
        return tracks        

    @pynvim.command("SpotifyInput", sync=True)
    def create_spotify_input(self):
        # Get the screen dimensions to calculate center
        screen_width = self.plugin.nvim.api.get_option('columns')
        screen_height = self.plugin.nvim.api.get_option('lines')

        # Set window size (e.g., 50 columns wide, 3 rows high)
        width = 50
        height = 3

        # Calculate the position (center of the screen)
        row = (screen_height - height) // 2
        col = (screen_width - width) // 2

        # Open the floating window
        opts = {
            'relative': 'editor',  # Relative to the editor (screen)
            'width': width,
            'height': height,
            'row': row,
            'col': col,
            'style': 'minimal',  # No borders, just the input field
            'border': 'none',  # No border around the window
        }

        # Open the window
        win_id = self.plugin.nvim.api.open_win(self.plugin.nvim.api.get_current_buf(), False, opts)
        buf = self.plugin.nvim.api.get_current_buf()
        self.plugin.nvim.api.buf_set_option(buf, "modifiable", True)
        self.plugin.nvim.api.buf_set_lines(self.plugin.nvim.api.get_current_buf(), 0, -1, False, ['Enter Spotify command:'])

        # Optionally, use input() to ask for user input (if it's a simple one-liner)
        user_input = self.plugin.nvim.api.input('Enter Spotify command: ')

        # Close the floating window after input
        self.plugin.nvim.api.win_close(win_id)

        # Process the user input (this could be your Spotify command)
        self.plugin.nvim.out_write(f"Spotify command entered: {user_input}\n")
