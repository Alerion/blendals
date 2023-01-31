import aud
import bpy
from bpy_types import Collection, Object

from blendals.load_song_from_file import load_song_from_file
from blendals.blender.create_controls_collection import create_controls_collection, create_control_object
from blendals.live_set_to_song import Song, Track
from blendals.config import settings


def main() -> None:
    # play_audio_file()
    song: Song = load_song_from_file()
    controls_collection = create_controls_collection()
    add_control_for_tracks(song, controls_collection)

    def stop_playback(scene):
        print(scene.frame_current)

    bpy.app.handlers.frame_change_pre.append(stop_playback)


def add_control_for_tracks(song: Song, controls_collection: Collection) -> None:
    for i, track in enumerate(song.tracks):
        control = bpy.context.scene.objects.get(track.id)
        if control is not None:
            continue

        control = create_control_object(track.id)
        control.location = (
            settings.CONTROLS_POSITION[0] + i,
            settings.CONTROLS_POSITION[1],
            settings.CONTROLS_POSITION[2],
        )
        controls_collection.objects.link(control)


def play_audio_file() -> None:
    device = aud.Device()
    sound = aud.Sound(settings.AUDIO_FILE_PATH)
    sound_buffered = aud.Sound.cache(sound)
    handle_buffered = device.play(sound_buffered)
    handle_buffered.position = 40  # seconds
    import time
    time.sleep(5)
    handle_buffered.stop()
