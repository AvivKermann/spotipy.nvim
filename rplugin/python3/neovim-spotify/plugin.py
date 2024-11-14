from pynvim.api.buffer import Buffer
from pynvim.api.nvim import Nvim
from pynvim.api.window import Window
from typing import Dict, Union
from .spotify import Spotify
import logging
from dataclasses import dataclass
from typing import Optional

@dataclass
class StatusBarIcons:
    track: str = "🎵"
    album: str = "📀"
    artist: str = "👤"
    play: str = "▶"
    pause: str = "❚❚"
    shuffle: str = "🔀"
    volume: str = "🔊"
    volume_mute: str = "🔇"
    volume_down: str = "🔉"
    volume_up: str = "🔊"
    device: str = "🔈"
    progress_complete: str = "-"
    progress_incomplete: str = "."
    progress_mark: str = "●"
    progress_bar_width: int = 32
    status_bar_width: int = 32

    @staticmethod
    def str_bar(progress_bar: str, title: str, artist: str, album: str) -> str:
        str_bar = f"""
        {StatusBarIcons.track} {title}\n
        {StatusBarIcons.artist} {artist}\n
        {StatusBarIcons.album} {album}\n
        {progress_bar}
        """

        return str_bar

class Plugin:
    def __init__(self, nvim: Nvim):
        self.nvim = nvim
        self.buffer: Union[None,Buffer] = None
        self.wins: Dict[Window, bool] = {}
        self.anchor: Union[Window, None] = None
        self.placeholder: Union[None,Buffer] = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.spotify = Spotify()



    def get_current_status(self) -> Optional[str]:
        track = self.spotify.get_currently_playing_track()
        if not track.exists:
            return

        progress_time_sec = track.progress_ms // 1000
        duration_time_sec = track.duration_ms // 1000
        progress_bar = self.get_progress_bar(progress_time_sec // duration_time_sec, StatusBarIcons.progress_bar_width)
        status_bar = StatusBarIcons.str_bar(
            progress_bar=progress_bar,
            title=track.title,
            artist=track.artist,
            album=track.album,
            )
        self.nvim.vars["testing"] = status_bar
        return status_bar
    

    def get_track_status(self) -> str:
        self.logger.info("Getting currently playing track")
        track = self.spotify.get_currently_playing_track()
        if track.exists:
            return f"{track.title} by {track.artist}"
        return ""
            



    def search(self, query: str, search_type: str = "track"):
        self.logger.info(f"Searching for track: {query}")
        tracks = self.spotify.search(query=query, search_type=search_type)
        return tracks

    def get_progress_bar(self, percentage: int, bar_length: int) -> str:
        progress_bar = ""
        middle = int(bar_length * percentage)
        progress_bar = StatusBarIcons.progress_complete * (middle - 1)
        progress_bar += StatusBarIcons.progress_mark
        progress_bar += StatusBarIcons.progress_incomplete * (bar_length - middle)
        return progress_bar 




