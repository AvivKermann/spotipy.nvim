from pynvim.api.nvim import Nvim
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pynvim
import time
import os
import logging

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

@dataclass 
class Track:
    exists: bool 
    title: str = ""
    artist: str = ""
    uri: str = ""
    duration_ms: int = 0
    progress_ms: int = 0

    def get_progress(self) -> str:
        progress_seconds = self.progress_ms // 1000
        progress_minutes = progress_seconds // 60
        progress_seconds = progress_seconds % 60
        return f"{progress_minutes}:{progress_seconds:02d}"

    def get_duration(self) -> str:
        duration_seconds = self.duration_ms // 1000
        duration_minutes = duration_seconds // 60
        duration_seconds = duration_seconds % 60
        return f"{duration_minutes}:{duration_seconds:02d}"


class Spotify:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cache = None
        try:
            self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id = os.getenv("CLIENT_ID"),
                client_secret = os.getenv("CLIENT_SECRET"),
                redirect_uri = os.getenv("REDIRECT_URI"),
                scope = "user-modify-playback-state user-read-playback-state user-read-currently-playing user-library-read user-library-modify",
                cache_path = self.cache,
                open_browser = False
            ))
        except Exception as e:
            self.logger.critical(f"Error initializing Spotify client: {e}")

    def get_currently_playing_track(self):
        try:
            current_track = self.spotify.current_user_playing_track()
            if current_track and current_track["item"]:
                track = Track(
                    title = current_track["item"]["name"],
                    artist = current_track["item"]["artists"][0]["name"],
                    uri = current_track["item"]["uri"],
                    duration_ms = current_track["item"]["duration_ms"],
                    progress_ms = current_track["progress_ms"],
                    exists = True
                )
                return track
            else:
                return Track(exists=False)

        except Exception as e:
            self.logger.error(f"Error fetching currently playing track: {e}")
            return Track(exists=False)

    def search(self, query: str, search_type: str = "track"):
        """ returns an array of tracks dict with title, artist, and uri."""
        try:
            tracks = []
            results = self.spotify.search(q=query, type=search_type, limit=20)

            # we don't care because spotify basically always returns something.
            for item in results[search_type + "s"]["items"]: # type: ignore
                tracks.append({
                    "title": item["name"],
                    "artist": item["artists"][0]["name"],
                    "uri": item["uri"]
                })
            return tracks

        except Exception as e:
            self.logger.error(f"Error searching for tracks: {e}")

    def play(self, uri: str):
        if not uri:
            self.logger.error("Must provide a uri to play.")
            return
        device_id = self.get_device_id()
        if not device_id:
            self.logger.error("No device found.")
            return

        try:
            self.spotify.start_playback(device_id=device_id, uris=[uri])
            self.logger.info(f"Playing {uri}")
        except Exception as e:
            self.logger.error(f"Error playing track: {e}")

    def toggle(self):
        try:
            playback = self.spotify.current_playback()
            if playback is None or not playback.get("device"):
                self.transfer_playback_to_device()

            if playback and playback.get("is_playing"):
                self.spotify.pause_playback()
                self.logger.info("Music paused.")
                return
            else:
                self.spotify.start_playback()
        except Exception as e:
            self.logger.error(f"Error in toggle: {e}")
            return

    def like(self, uri: str):
        pass

    def transfer_playback_to_device(self):
        devices = self.spotify.devices()
        if devices and "devices" in devices:
            for device in devices["devices"]:
                if device["type"] == "Computer":
                    self.spotify.transfer_playback(device["id"], force_play=False)
                    self.logger.info(f"Transferred playback to {device['name']}")
                    break
            else:
                self.logger.info("No computer device found.")
        else:
            self.logger.info("No devices found.")

    def get_device_id(self):
        devices = self.spotify.devices()
        if devices and "devices" in devices:
            for device in devices["devices"]:
                if device["type"] == "Computer":
                    return device["id"]

    def next(self):
        try:
            # make sure the device is connected.
            self.transfer_playback_to_device()
            self.spotify.next_track()
            playback = self.spotify.current_playback()

            # auto start the track after skipping
            if playback and not playback.get("is_playing"):
                self.spotify.start_playback()
            self.logger.info("Skipped to the next track.")
        except Exception as e:
            self.logger.error(f"Error skipping to the next track: {e}")

    def prev(self):
        try:
            # make sure the device is connected.
            self.transfer_playback_to_device()
            self.spotify.previous_track()
            playback = self.spotify.current_playback()

            # auto start the track after going back
            if playback and not playback.get("is_playing"):
                self.spotify.start_playback()
            self.logger.info("Skipped to the previous track.")
        except Exception as e:
            self.logger.error(f"Error skipping to the previous track: {e}")

class Plugin:
    WIDTH = 48
    HEIGHT = 3
    def __init__(self, nvim: Nvim):
        self.nvim = nvim
        self.spotify = Spotify()
        self.logger = logging.getLogger(__name__)



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

