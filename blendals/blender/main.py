from bpy_types import Collection

from blendals.blender.audio import add_audio_to_sequence_editor
from blendals.blender.create_controls_collection import create_controls_collection
from blendals.song import Song
from blendals.load_song_from_file import load_song_from_file
from blendals.blender.curve_generators import MidiTrackToCurve, AudioTrackToCurve
from blendals.blender.timeline_markers import add_timeline_markers_for_bars
from blendals.blender.control import Control


def main() -> None:
    song: Song = load_song_from_file()
    add_timeline_markers_for_bars()
    add_audio_to_sequence_editor()

    controls_collection = create_controls_collection()
    create_extrude_control(song, controls_collection)
    create_material_control(song, controls_collection)


def create_extrude_control(song: Song, controls_collection: Collection) -> None:
    extrude_control = Control("Extrude Control")
    extrude_control.create_blender_object(controls_collection)
    kick_track = song.get_midi_track("Kick:36")
    curve_generator = MidiTrackToCurve(kick_track, value_range=5)
    extrude_control.animate(curve_generator, data_path="scale", scale_index=0)
    extrude_control.animate(curve_generator, data_path="scale", scale_index=1)
    extrude_control.animate(curve_generator, data_path="scale", scale_index=2)


def create_material_control(song: Song, controls_collection: Collection) -> None:
    extrude_control = Control("Material Control")
    extrude_control.create_blender_object(controls_collection)
    kick_track = song.get_midi_track("Percs:36")
    curve_generator = MidiTrackToCurve(kick_track, min_value=0, note_release=2)
    extrude_control.animate(curve_generator, data_path="scale", scale_index=0)
    extrude_control.animate(curve_generator, data_path="scale", scale_index=1)
    extrude_control.animate(curve_generator, data_path="scale", scale_index=2)


    #
    #
    # for i, track in enumerate(song.midi_tracks + song.audio_tracks):
    #     animation_generator = TRACK_ANIMATION_GENERATORS.get(track.id)
    #     if animation_generator is None:
    #         print(f"Animation generator is not found for track {track.id}")
    #         continue
    #
    #     print("Animation generator is found for track {track.id}")
    #
    #     control = bpy.context.scene.objects.get(track.id)
    #     if control is None:
    #         control = create_control_object(track.id)
    #         control.location = (
    #             settings.CONTROLS_POSITION[0],
    #             settings.CONTROLS_POSITION[1],
    #             settings.CONTROLS_POSITION[2],
    #         )
    #         controls_collection.objects.link(control)
    #
    #     animation_generator.generate(control, track)
