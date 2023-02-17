import orjson
import dacite

from blendals.song import Song
from blendals.config import settings


def load_song_from_file() -> Song:
    with open(settings.SONG_FILE_PATH, "r") as song_file:
        data = orjson.loads(song_file.read())
    song: Song = dacite.from_dict(data_class=Song, data=data)
    return song


if __name__ == "__main__":
    load_song_from_file()
