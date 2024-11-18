import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)


@dataclass 
class Track:
    exists: bool 
    title: str = ""
    artist: str = ""
    album: str = ""
    device: str = ""
    uri: str = ""
    volume: int = 100
    duration_ms: int = 0
    playing: bool = False
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
        try:
            self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id = os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret = os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI"),
                scope = "user-modify-playback-state user-read-playback-state user-read-currently-playing user-library-read user-library-modify",
                cache_path ="/tmp/.spotify_cache"
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
                    exists = True,
                    album = current_track["item"]["album"]["name"],
                    playing = current_track["is_playing"]
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

    def play(self, uri: str, device_id: Optional[str] = None):
        if not uri:
            self.logger.error("Must provide a uri to play.")
            return

        device_id = device_id or None
        try:
            # We do this to avoid spotify's stupid cancel autoplay if played a track by uri.
            # This way we technically never actually play by uri, we add and skip to it.
            # I hate this as well as you... but this is what we get.
            # I added the actually command to just play by uri but it's commented out.
            # self.spotify.start_playback(device_id=device_id, uris=[uri])

            self.add_to_queue(uri, device_id)
            self.next()
            self.logger.info(f"Playing {uri}")
        except Exception as e:
            self.logger.error(f"Error playing track: {e}")

    def toggle(self,playback: Optional[Dict[Any, Any]], device_id: Optional[str] = None):
        try:
            if not playback or not playback["is_playing"]:
                self.spotify.start_playback(device_id=device_id)
                self.logger.info("Music started.")

            else:
                assert playback is not None
                # we can assert this because if playback is None we will start playback
                if playback["is_playing"]:
                    self.spotify.pause_playback(device_id=device_id)
                    self.logger.info("Music paused.")

        except Exception as e:
            self.logger.error(f"Error in toggle: {e}")
            return

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
            self.spotify.next_track()
            playback = self.spotify.current_playback()
            # auto start the track after skipping
            assert playback is not None
            if not playback["is_playing"]:
                self.spotify.start_playback()
                self.logger.info("Skipped to the next track.")
        except Exception as e:
            self.logger.error(f"Error skipping to the next track: {e}")

    def prev(self):
        try:
            self.spotify.previous_track()
            playback = self.spotify.current_playback()
            assert playback is not None
            if not playback["is_playing"]:
                self.spotify.start_playback()
                self.logger.info("Skipped to the previous track.")
        except Exception as e:
             self.logger.error(f"Error skipping to the previous track: {e}")

    def get_playlist(self):
        queue = self.spotify.queue()
        playlist = []
        try:
            assert queue is not None
            tracks = [(track["name"], track["artists"][0]["name"], track["uri"]) for track in queue["queue"]]
            for track in tracks:
                title, artist, uri = track
                playlist.append({
                    "title": title,
                    "artist": artist,
                    "uri": uri
                })

            return playlist

        except AssertionError:
            # only return None if the queue is empty.
            return None

        except Exception:
            return None

    def get_devices(self):
        try:
            devices = []
            results = self.spotify.devices()
            assert results is not None
            for device in results["devices"]:
                devices.append({
                    "name": device["name"],
                    "id": device["id"]})

            return devices

        except Exception:
            return []

    def add_to_queue(self, uri: str, device_id: Optional[str] = None):
        if not uri:
            self.logger.error("Must provide a uri to add to queue.")
            return
        device_id = device_id or None
        try:
            self.spotify.add_to_queue(uri=uri, device_id=device_id)
        except Exception:
            self.logger.error("Error adding to queue")




