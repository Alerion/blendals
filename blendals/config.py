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
    FIRST_VIDEO_FRAME: int = 1
    FRAME_RATE_FPS: int = 24
    # The first bar is 1
    SONG_TEMPO: int = 120
    SONG_BAR_SIZE_BEATS: int = 4
    SONG_START_BAR: float = 1


settings = Settings()
