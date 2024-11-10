import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import logging
from dataclasses import dataclass
logging.basicConfig(level=logging.INFO)


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
                cache_path ="~/.cache/.spotify_cache"
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

