from .command import NeovimSpotify
import subprocess

def get_currently_playing_track(self: NeovimSpotify):
    response = subprocess.run(["spt", "playback", "-s", "-f", "%t by %a"])
    if response.returncode != 0:
        self.nvim.command("echo 'Error fetching current track'")

    self.nvim.command(f"echo '{response.stdout.decode().strip()}'")
