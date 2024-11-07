from __init__ import NeovimSpotify
import subprocess

def fetch_currently_playing_track(self: NeovimSpotify) -> None:
    self.logger.info("Fetching currently playing track")

    res = subprocess.run("spt playback -s -f %t", shell=True, capture_output=True)
    if res.returncode != 0:
        self.logger.error("Failed to fetch currently playing track")
        return
    track = res.stdout.decode().strip()
    show_currently_playing_track(self, track)


def show_currently_playing_track(self: NeovimSpotify, cur_playing: str) -> None:
    self.logger.info("Creating CurrentlyPlaying")
    
    buf = self.nvim.api.create_buf(False, True)
    
    
    top_border = f"╭{'─' * ((self.WIDTH - 19) // 2)} Currently Playing {'─' * ((self.WIDTH - 21) // 2)}╮".encode('utf-8')
    empty_line = f"│ 墳{' ' * (self.WIDTH - 5)}│".encode('utf-8')
    bot_border = f"╰{'─' * (self.WIDTH - 2)}╯".encode('utf-8')
    
    replacement = [top_border, empty_line, bot_border]
    
    opts = {
        'Relative': 'win',
        'Win': self.anchor,
        'Width': self.WIDTH,
        'Height': self.HEIGHT,
        'BufPos': [0, 0],
        'Row': -3,
        'Col': -2,
        'Style': 'minimal',
        'ZIndex': 50,
        'Focusable': False
    }
    
    self.nvim.api.buf_set_lines(buf, 0, -1, True, replacement)
    
    self.nvim.api.buf_set_lines(buf, 1, 7, 1, len(cur_playing) + 7, [cur_playing.encode('utf-8')])

    self.nvim.api.buf_set_option(buf, 'modifiable', False)
    self.nvim.api.buf_set_option(buf, 'bufhidden', 'wipe')
    self.nvim.api.buf_set_option(buf, 'buftype', 'nofile')
    
    win = self.nvim.api.open_window(buf, False, opts)
    self.wins[win] = True
    
    self.nvim.api.win_set_option(win, 'winhl', 'Normal:SpotifyBorder')
    self.nvim.api.win_set_option(win, 'winblend', 0)
    self.nvim.api.win_set_option(win, 'foldlevel', 100)

def create_input(self: NeovimSpotify) -> None:
    self.logger.info("Creating input buffer")
    buf = self.nvim.api.create_buf(False, True)
    if not buf:
        self.logger.error("Failed to create input buffer")
        return

    self.buffer = buf

