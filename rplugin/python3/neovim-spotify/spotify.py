import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import logging
logging.basicConfig(level=logging.INFO)

class Spotify:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id = os.getenv("CLIENT_ID"),
                client_secret = os.getenv("CLIENT_SECRET"),
                redirect_uri = os.getenv("REDIRECT_URI"),
                scope = "user-modify-playback-state user-read-playback-state user-read-currently-playing user-library-read user-library-modify",
                cache_path=".spotify_cache"
            ))
        except Exception as e:
            self.logger.critical(f"Error initializing Spotify client: {e}")

    def get_currently_playing_track(self):
        try:
            current_track = self.spotify.current_user_playing_track()
            if current_track and current_track["item"]:
                track_name = current_track["item"]["name"]
                artist_name = current_track["item"]["artists"][0]["name"]
                return f"{track_name} by {artist_name}"
            else:
                return "No track currently playing"
        except Exception as e:
            self.logger.error(f"Error fetching currently playing track: {e}")
            return "Error fetching track"

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
        if devices and 'devices' in devices:
            for device in devices['devices']:
                if device["type"] == "Computer":
                    self.spotify.transfer_playback(device["id"], force_play=False)
                    self.logger.info(f"Transferred playback to {device['name']}")
                    break
            else:
                self.logger.info("No computer device found.")
        else:
            self.logger.info("No devices found.")

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
