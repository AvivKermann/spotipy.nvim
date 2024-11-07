from __init__ import NeovimSpotify

HEIGHT = 48
WIDTH = 3


def create_placeholder(self: NeovimSpotify) -> None:

    self.logger.info("Creating placeholder buffer")
    buf = self.nvim.api.create_buf(False, True)
    if not buf:
        self.logger.error("Failed to create placeholder buffer")
        return

    self.placeholder = buf

    text = " Spotify Search: Tracks "
    repeat_w = (WIDTH - len(text) - 1) // 2
    border = "─" * repeat_w

    top_border = f"╭{border}{text}{border}╮"
    empty_line = f"│ › {' ' * (WIDTH - 5)}│"
    bot_border = f"╰{'─' * (WIDTH - 2)}╯"

    replacement = [top_border, empty_line, bot_border]

    self.nvim.api.buf_set_lines(buf, 0, -1, True, replacement)

    self.nvim.api.buf_set_option(buf, "modifiable", False)
    self.nvim.api.buf_set_option(buf, "bufhidden", "wipe")
    self.nvim.api.buf_set_option(buf, "buftype", "nofile")

    opts = {
        "relative": "win",
        "width": WIDTH,
        "height": HEIGHT,
        "row": 0.5,
        "col": -2,
        "anchor": "NW",
        "style": "minimal",
        "zindex": 50,
        "focusable": False,
    }

    win = self.nvim.api.open_win(buf, False, opts)
    self.wins[win] = True

    self.nvim.api.win_set_option(win, "winhl", "Normal:SpotifyBorder")
    self.nvim.api.win_set_option(win, "winblend", 0)
    self.nvim.api.win_set_option(win, "foldlevel", 100)

def create_anchor(self: NeovimSpotify) -> None:
    self.logger.info("Creating anchor")
    buf = self.nvim.api.create_buf(False, True)
    uis = self.nvim.api.list_uis()
    if not buf:
        self.logger.error("Failed to create anchor buffer")
        return
    if not uis:
        self.logger.error("Failed to get ui list")
        return
    row = (uis[0]['height'] / 2) - (HEIGHT / 2)
    col = (uis[0]['width'] / 2) - (WIDTH / 2) + 1.5

    opts = {
        "relative": "editor",
        "anchor": "NW",
        "width": 1,
        "height": 1,
        "row": row,
        "col": col,
        "style": "minimal",
        "zindex": 50,
        "focusable": False,
    }

    self.nvim.api.buf_set_option(buf, "bufhidden", "wipe")
    self.nvim.api.buf_set_option(buf, "buftype", "nofile")

    win = self.nvim.api.open_win(buf, False, opts)
    self.anchor = win
    self.wins[win] = True

