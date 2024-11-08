import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()
class Spotify:
    def __init__(self):
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id = os.getenv("CLIENT_ID"),
            client_secret = os.getenv("CLIENT_SECRET"),
            redirect_uri = os.getenv("REDIRECT_URI"),
            scope = "user-modify-playback-state user-read-playback-state user-read-currently-playing user-library-read user-library-modify",
            )
        )

    def get_currently_playing_track(self):
        current_track = self.spotify.current_user_playing_track()
        if current_track:
            track_name = current_track["item"]["name"]
            artist_name = current_track["item"]["artists"][0]["name"]
            return f"{track_name} by {artist_name}"

        return "No track currently playing"

