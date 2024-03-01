import json

import dacite

from blendals_.song import Song, MidiTrack
from blendals_.config import settings


def load_song_from_file() -> Song:
    with open(settings.SONG_FILE_PATH, "r") as song_file:
        data = json.loads(song_file.read())
    song: Song = dacite.from_dict(data_class=Song, data=data)
    return song


if __name__ == "__main__":
    load_song_from_file()
