import bpy
from bpy_types import Collection, Object

from blendals.load_song_from_file import load_song_from_file
from blendals.blender.create_controls_collection import create_controls_collection, create_control_object
from blendals.live_set_to_song import Song, Track
from blendals.config import settings


def main() -> None:
    song: Song = load_song_from_file()
    controls_collection = create_controls_collection()
    add_control_for_tracks(song, controls_collection)
    add_audio_to_sequence_editor()


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


def add_audio_to_sequence_editor(channel: int = 1, frame_start: int = 1) -> None:
    scene = bpy.context.scene

    # Create sequences editor
    if not scene.sequence_editor:
        scene.sequence_editor_create()

    # Remove existing sequence
    existing_sequence = None
    for sequence in scene.sequence_editor.sequences.values():
        if sequence.channel == channel:
            existing_sequence = sequence
            break

    if existing_sequence is not None:
        scene.sequence_editor.sequences.remove(existing_sequence)

    # Add audio file as a sequence
    # TODO: Get frame_start from animation properties
    scene.sequence_editor.sequences.new_sound("Audio track", settings.AUDIO_FILE_PATH, channel, frame_start)
