import os.path
from dataclasses import dataclass

from blendals.types import Location

PACKAGE_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = os.path.join(PACKAGE_ROOT, "..")


@dataclass
class Settings:
    SONG_FILE_PATH: str = os.path.join(PROJECT_ROOT, "song.json")
    AUDIO_FILE_PATH: str = os.path.join(PROJECT_ROOT, "song.wav")
    LIVE_SET_CONTROLS_COLLECTION: str = "LiveSetControls"
    CONTROLS_POSITION: Location = (10, 10, 0)


settings = Settings()
