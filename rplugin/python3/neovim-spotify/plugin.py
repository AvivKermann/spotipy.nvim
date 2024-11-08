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
        # response = subprocess.run("spt playback -s -f '%t by %a'", shell=True, capture_output=True)
        # if response.returncode != 0:
        #     self.logger.error("Error getting currently playing track")
        #     return
        # track = response.stdout.decode().strip()
        track = self.spotify.get_currently_playing_track()
        self.nvim.command(f"echo '{track}'")

    def start(self):
        self.config_plugin()

        self.create_placeholder()
        self.get_currently_playing_track()
        self.create_input()

    def config_plugin(self) -> None:
        
        self.logger.info("Configuring plugin")
        self.nvim.command("hi SpotifyBorder guifg=#1db954")
        self.nvim.command("hi SpotifyText guifg=#1ed760")
        self.nvim.command("hi SpotifySelection guifg=#191414 guibg=#1ed760")

    def create_placeholder(self) -> None:
        self.logger.info("Creating placeholde")
        buf = self.nvim.api.create_buf(False, True)
        if not buf:
            self.logger.error("Error creating buffer")
            return
        self.placeholder = buf

        header = " Spotify Search "
        width_spacer = (self.WIDTH - len(header) - 1) // 2
        border = "-" * width_spacer
        top_border = f"╭{border}{header}{border}╮".encode()
        empty_line = f"│ › {' ' * (self.WIDTH - 5)}│".encode()
        bot_border = f"╰{'─' * (self.WIDTH - 2)}╯".encode()
        replace_lines = [top_border, empty_line, bot_border]

        opts = {
            "relative": "win",
            "win": self.anchor,
            "width": self.WIDTH,
            "height": self.HEIGHT,
            "bufpos": [0, 0],
            "row": 0.5,
            "col": -2,
            "style": "minimal",
            "zindex": 50,
            "focusable": False,
        }

        self.nvim.api.buf_set_lines(buf, 0, -1, True, replace_lines)

        self.nvim.api.buf_set_option(buf, "modifiable", False)
        self.nvim.api.buf_set_option(buf, "bufhidden", "wipe")
        self.nvim.api.buf_set_option(buf, "buftype", "nofile")

        win = self.nvim.api.open_win(buf, False, opts)
        self.wins[win] = True

        self.nvim.api.win_set_option(win, "winhl", "Normal:SpotifyBorder")
        self.nvim.api.win_set_option(win, "winblend", 0)
        self.nvim.api.win_set_option(win, "foldlevel", 100)

    def create_input(self) -> None:
        self.logger.info("Creating input")
