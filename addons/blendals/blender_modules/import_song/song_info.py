import bpy
import bpy_types

from blendals.blnder_utils.enums import  WMReport, OperatorReturn, OperatorTypeFlag
from bpy_extras.io_utils import ImportHelper

__all__ = (
    "BlendalsSongProperties",
    "BLENDALS_PT_SongInfo",
    "BLENDALS_OT_AddSongAudioTrack",
)


class BLENDALS_OT_AddSongAudioTrack(bpy.types.Operator, ImportHelper):
    bl_idname = "blendals.add_song_audio_track"
    bl_label = "Add Song Audio Track"
    bl_options = {OperatorTypeFlag.REGISTER}

    @classmethod
    def poll(cls, context):
        return is_song_object(context.object)

    def execute(self, context: bpy_types.Context) -> set[OperatorReturn]:
        scene = context.scene

        # Create sequences editor.
        if not scene.sequence_editor:
            scene.sequence_editor_create()

        # Find empty channel.
        available_channels = list(range(1, 129))
        for sequence in scene.sequence_editor.sequences.values():
            if sequence.channel in available_channels:
                available_channels.remove(sequence.channel)

        if len(available_channels) == 0:
            self.report({WMReport.WARNING}, "No empty channels to add a song audio.")
            return {OperatorReturn.CANCELLED}

        # Add new sound for a song audio.
        scene.sequence_editor.sequences.new_sound(
            "Song Audio", self.filepath, available_channels[0], scene.frame_start
        )

        return {OperatorReturn.FINISHED}


class BlendalsSongProperties(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")
    bar_start: bpy.props.IntProperty(name="Start Bar", default=1, min=1)
    bpm: bpy.props.IntProperty(name="BPM")
    time_signature_numerator: bpy.props.IntProperty(name="Time Signature Numerator")
    length_in_bars: bpy.props.FloatProperty(name="Length in bars")

    @classmethod
    def register(cls):
        bpy.types.Object.blendals_song = bpy.props.PointerProperty(
            name="Blendals Song",
            description="Blendals Song Properties",
            type=cls,
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Object.blendals_song


def is_song_object(obj: bpy_types.Object | None) -> bool:
    if obj is None:
        return False
    return bool(obj.blendals_song.name)


class BLENDALS_PT_SongInfo(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Blendals Song Info"
    bl_idname = "OBJECT_PT_blendals_song_info"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context) -> bool:
        if context.object is None:
            return False

        if not context.object.blendals_song.name:
            return False

        return True

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text=f"Song: {obj.blendals_song.name}")
        row = layout.row()
        row.prop(obj.blendals_song, "bpm")
        row.prop(obj.blendals_song, "length_in_bars")
        row = layout.row()
        row.prop(obj.blendals_song, "time_signature_numerator")
        row = layout.row()
        row.operator(BLENDALS_OT_AddSongAudioTrack.bl_idname)
