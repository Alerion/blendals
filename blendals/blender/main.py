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
    curve_generator = MidiTrackToCurve(kick_track)
    extrude_control.animate_scale(curve_generator)


def create_material_control(song: Song, controls_collection: Collection) -> None:
    material_control = Control("Material Control")
    material_control.create_blender_object(controls_collection)
    kick_track = song.get_midi_track("Percs:36")
    curve_generator = MidiTrackToCurve(kick_track, note_release=2)
    material_control.animate_scale(curve_generator)
