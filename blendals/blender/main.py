import bpy
from bpy_types import Collection, Object

from blendals.blender.audio import add_audio_to_sequence_editor
from blendals.blender.create_controls_collection import (
    create_controls_collection,
    create_control_object,
)
from blendals.config import settings
from blendals.song import Song, MidiTrack
from blendals.load_song_from_file import load_song_from_file
from blendals.blender.animations import ScaleAnimation
from blendals.blender.curve_generators import MidiTrackToCurve, AudioTrackToCurve
from blendals.blender.timeline_markers import add_bars_markers


TRACK_ANIMATION_GENERATORS = {
    "Kick:36": ScaleAnimation(MidiTrackToCurve(max_value=3)),
    "Percs:36": ScaleAnimation(MidiTrackToCurve(min_value=0, max_value=1, note_release=2)),
    "Pads:left_channel": ScaleAnimation(AudioTrackToCurve(max_value=3)),
    "Effects:left_channel": ScaleAnimation(AudioTrackToCurve(max_value=3)),
}


def main() -> None:
    song: Song = load_song_from_file()
    add_bars_markers()
    controls_collection = create_controls_collection()
    add_control_for_tracks(song, controls_collection)
    add_audio_to_sequence_editor()


def add_control_for_tracks(song: Song, controls_collection: Collection) -> None:
    for i, track in enumerate(song.midi_tracks + song.audio_tracks):
        animation_generator = TRACK_ANIMATION_GENERATORS.get(track.id)
        if animation_generator is None:
            print(f"Animation generator is not found for track {track.id}")
            continue

        print("Animation generator is found for track {track.id}")

        control = bpy.context.scene.objects.get(track.id)
        if control is None:
            control = create_control_object(track.id)
            control.location = (
                settings.CONTROLS_POSITION[0],
                settings.CONTROLS_POSITION[1],
                settings.CONTROLS_POSITION[2],
            )
            controls_collection.objects.link(control)

        animation_generator.generate(control, track)
