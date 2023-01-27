import gzip
import os.path
import xml.dom.minidom
from pathlib import Path

import typer
from lxml import etree
from rich import print

from blendals.live_set_parser import parse_als_file_content
from blendals.utils.xml import save_xml_to_file

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
    content = gzip.decompress(als_file.read_bytes())
    content = content.replace(b"\t", b"")
    content = content.replace(b"\n", b"")
    live_set_xml = etree.fromstring(content)
    live_set = parse_als_file_content(live_set_xml)

    # track = live_set.tracks[2]
    # if track._element is not None:
    #     save_xml_to_file(track._element, "track.xml")
    # print(track)


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
