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
    CONTROLS_POSITION: Location = (0, 0, 0)
    # TODO: Get from project data
    START_FRAME: int = 1
    FRAME_RATE_FPS: int = 24


settings = Settings()
