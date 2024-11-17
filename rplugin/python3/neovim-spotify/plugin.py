from pynvim.api.buffer import Buffer
from pynvim.api.nvim import Nvim
from pynvim.api.window import Window
from typing import Dict, Union
from .spotify import Spotify, Track
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
    progress_complete: str = "─"
    progress_incomplete: str = "┈"
    progress_mark: str = "●"
    progress_bar_width: int = 28
    status_bar_width: int = 34
    time: str = "🕒"

    @staticmethod
    def str_bar(progress_bar: str, track: Track) -> str:
        state = StatusBarIcons.play if track.playing else StatusBarIcons.pause
        str_bar = (
            f" {StatusBarIcons.track} {track.title}\n"
            f" {StatusBarIcons.artist} {track.artist}\n"
            f" {StatusBarIcons.album} {track.album}\n\n"
            f" {StatusBarIcons.time} {track.get_progress()}  /  {track.get_duration()}\n"
            f" {state} {progress_bar}\n"
        )

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

        progress_bar = self.get_progress_bar(track)
        status_bar = StatusBarIcons.str_bar(progress_bar, track)
        return status_bar
    

    def get_track_status(self) -> str:
        self.logger.info("Getting currently playing track")
        track = self.spotify.get_currently_playing_track()
        button = StatusBarIcons.play if track.playing else StatusBarIcons.pause

        if track.exists:
            return f"{button} | {track.title} by {track.artist}"
        return ""
            



    def search(self, query: str, search_type: str = "track"):
        self.logger.info(f"Searching for track: {query}")
        tracks = self.spotify.search(query=query, search_type=search_type)
        return tracks

    def get_progress_bar(self, track: Track) -> str:
        progress = self.time_str_to_seconds(track.get_progress())
        duration = self.time_str_to_seconds(track.get_duration())
        bar_length = StatusBarIcons.progress_bar_width  # Total length of the progress bar

        if duration == 0:
            return StatusBarIcons.progress_incomplete * bar_length
        progress_position = int((progress / duration) * bar_length)
        progress_bar = (
            StatusBarIcons.progress_complete * progress_position
            + StatusBarIcons.progress_mark
            + StatusBarIcons.progress_incomplete * (bar_length - progress_position - 1)
        )
        return progress_bar

    def time_str_to_seconds(self,time_str: str) -> int:
        minutes, seconds = time_str.split(":")
        return int(minutes) * 60 + int(seconds)




