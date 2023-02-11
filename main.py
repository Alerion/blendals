import gzip
import xml.dom.minidom
from pathlib import Path

import orjson
import typer

from blendals.live_set_parser import LiveSetParser
from blendals.utils.xml import save_xml_to_file
from blendals.live_set_to_song import live_set_to_song
from blendals.config import settings

app = typer.Typer()


@app.command()
def parse(
    als_file: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    )
):
    live_set_parser = LiveSetParser(als_file)
    live_set = live_set_parser.get_live_set()

    save_xml_to_file(live_set._element, "live_set.xml")
    # track = live_set.tracks[2]
    # if track._element is not None:
    #     save_xml_to_file(track._element, "track.xml")
    # print(track)

    song = live_set_to_song(live_set)
    with open(settings.SONG_FILE_PATH, "w") as f:
        json = orjson.dumps(song, option=orjson.OPT_INDENT_2)
        f.write(json.decode("utf-8"))


@app.command()
def save_als_xml_to_file(
    als_file: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    )
):
    content = gzip.decompress(als_file.read_bytes())
    content = content.replace(b"\t", b"")
    content = content.replace(b"\n", b"")

    live_set_xml = xml.dom.minidom.parseString(content)
    pretty_content = live_set_xml.toprettyxml()
    with open("content.xml", "w") as f:
        f.write(pretty_content)


if __name__ == "__main__":
    app()
