import os
import json

import dacite
import json

import bpy
import bpy_types

from blendals.curve_generators.frame_calculator import FrameCalculator
from bpy_extras.io_utils import ImportHelper

from blendals.data.song import Song, MidiTrack
from blendals.blnder_utils.collection import create_or_get_collection
from blendals.blnder_utils.enums import EmptyDrawType

__all__ = (
    "BLENDALS_OT_ParseSong",
    "BLENDALS_PT_ParseSong",
)

SONG_COLLECTION_NAME = "Songs"


class BLENDALS_OT_ParseSong(bpy.types.Operator, ImportHelper):
    bl_idname = "blendals.import_song"
    bl_label = "Parse Song"

    filter_glob: bpy.props.StringProperty(default='*.json', options={'HIDDEN'})
    add_timeline_markers: bpy.props.BoolProperty(
        name="Add Timeline Markers",
        description="Add timeline markers for song bars. Useful for debugging.",
        default=False
    )
    bar_start: bpy.props.IntProperty(
        name="Start Bar",
        default=1,
        min=1
    )

    def execute(self, context: bpy_types.Context) -> set[str]:
        # See https://docs.blender.org/api/current/bpy.types.WindowManager.html#bpy.types.WindowManager.fileselect_add
        filename, extension = os.path.splitext(self.filepath)
        _, filename = os.path.split(filename)
        print('Selected file:', self.filepath)
        print('File name:', filename)
        print('File extension:', extension)

        with open(self.filepath, "r") as song_file:
            song_data = json.loads(song_file.read())
            song: Song = dacite.from_dict(data_class=Song, data=song_data)

        midi_tracks_count = len(song_data["midi_tracks"])
        audio_tracks_count = len(song_data["audio_tracks"])

        self.report({"INFO"}, f"{midi_tracks_count} MIDI and {audio_tracks_count} audio tracks parsed!")

        # Create object for song.
        songs_collection = create_or_get_collection(SONG_COLLECTION_NAME)
        song_obj = create_song_object(songs_collection, song, self.bar_start)

        if self.add_timeline_markers:
            clear_song_bars_timeline_markers(context)
            frame_calculator = FrameCalculator.create_from_song(song_obj, context.scene)
            add_song_bars_timeline_markers(frame_calculator)

        return {'FINISHED'}


def add_song_bars_timeline_markers(frame_calculator: FrameCalculator, bars_number: int = 10) -> None:
    for i in range(bars_number):
        current_bar = frame_calculator.song_bar_start + i - 1
        if current_bar <= 1:
            current_bar = 1

        beat = (current_bar - 1) * frame_calculator.song_time_signature_numerator
        frame = frame_calculator.beat_to_frame(beat)
        bpy.context.scene.timeline_markers.new(name=f"bar:{current_bar}", frame=frame)


def clear_song_bars_timeline_markers(context: bpy_types.Context):
    timeline_markers_to_remove = []
    for timeline_marker in context.scene.timeline_markers.values():
        if timeline_marker.name.startswith("bar:"):
            timeline_markers_to_remove.append(timeline_marker)

    for timeline_marker in timeline_markers_to_remove:
        context.scene.timeline_markers.remove(timeline_marker)


def create_song_object(songs_collection: bpy_types.Collection, song: Song, bar_start: int) -> bpy_types.Object:
    song_object = bpy.data.objects.new(name=song.name, object_data=None)
    song_object.empty_display_type = EmptyDrawType.PLAIN_AXES
    song_object.empty_display_size = 1
    songs_collection.objects.link(song_object)

    song_object.blendals_song.name = song.name
    song_object.blendals_song.bpm = song.bpm
    song_object.blendals_song.time_signature_numerator = song.time_signature_numerator
    song_object.blendals_song.bar_start = bar_start
    song_object.blendals_song.length_in_bars = song.length_in_bars

    for midi_track in song.midi_tracks:
        midi_track_object = create_midi_track_object(midi_track)
        songs_collection.objects.link(midi_track_object)
        midi_track_object.parent = song_object
        midi_track_object.animation_data_clear()
        midi_track_object.animation_data_create()

    return song_object


def create_midi_track_object(midi_track: MidiTrack) -> bpy_types.Object:
    midi_track_object = bpy.data.objects.new(name=f"midi_track_{midi_track.id}", object_data=None)
    midi_track_object.empty_display_type = EmptyDrawType.PLAIN_AXES
    midi_track_object.empty_display_size = 1

    midi_track_object.blendals_midi_track.track_id = midi_track.id
    midi_track_object.blendals_midi_track.notes_number = len(midi_track.notes)
    midi_track_object.blendals_midi_track.raw_data = json.dumps(midi_track).decode()

    return midi_track_object


class BLENDALS_PT_ParseSong(bpy.types.Panel):
    bl_idname = "BLENDALS_PT_ParseSong"
    bl_label = "Parse Song"
    bl_category = "Blendals"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    # bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context: bpy_types.Context) -> None:
        layout = self.layout

        col = layout.column(align=True)
        col.operator(BLENDALS_OT_ParseSong.bl_idname, text="Parse Song")
