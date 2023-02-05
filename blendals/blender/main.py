import bpy
from bpy_types import Collection, Object

from blendals.blender.audio import add_audio_to_sequence_editor
from blendals.blender.create_controls_collection import create_controls_collection, create_control_object
from blendals.config import settings
from blendals.live_set_to_song import Song, Track
from blendals.load_song_from_file import load_song_from_file
from blendals.blender.controls_animation_generator import ScaleControlAnimationGenerator


TRACK_ANIMATION_GENERATORS = {
    "Kick:36": ScaleControlAnimationGenerator("Kick:36", max_scale=3),
    "Percs:36": ScaleControlAnimationGenerator("Percs:36", min_scale=0, max_scale=1, note_release=2),
}


def main() -> None:
    song: Song = load_song_from_file()
    controls_collection = create_controls_collection()
    add_control_for_tracks(song, controls_collection)
    add_audio_to_sequence_editor()


def add_control_for_tracks(song: Song, controls_collection: Collection) -> None:
    for i, track in enumerate(song.tracks):
        animation_generator = TRACK_ANIMATION_GENERATORS.get(track.id)
        if animation_generator is None:
            continue

        control = bpy.context.scene.objects.get(track.id)
        if control is not None:
            continue

        control = create_control_object(track.id)
        control.location = (
            settings.CONTROLS_POSITION[0],
            settings.CONTROLS_POSITION[1],
            settings.CONTROLS_POSITION[2],
        )
        controls_collection.objects.link(control)

        animation_generator.generate(control, song)
