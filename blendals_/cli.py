import typer
from rich import print

from blendals_.load_song_from_file import load_song_from_file


app = typer.Typer()


@app.command("validate_song_json_file")
def validate_song_json_file():
    """
    python -m blendals_.cli validate_song_json_file
    """
    song = load_song_from_file()
    print(song)


@app.command("validate_files")
def validate_files():
    print("TODO")


if __name__ == "__main__":
    app()
