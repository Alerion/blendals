import dacite
import orjson

import bpy
import bpy_types

from blendals.data.song import MidiTrack

__all__ = (
    "BlendalsMidiTrackProperties",
    "BLENDALS_PT_MidiTrackInfo",
    "BLENDALS_OT_ApplyAnimation"
)


class BlendalsMidiTrackProperties(bpy.types.PropertyGroup):
    track_id: bpy.props.StringProperty(name="ID")
    notes_number: bpy.props.IntProperty(name="Notes number")
    raw_data: bpy.props.StringProperty(name="Raw data")

    @property
    def midi_track(self) -> MidiTrack:
        midi_track_data = orjson.loads(self.raw_data)
        return dacite.from_dict(data_class=MidiTrack, data=midi_track_data)

    @classmethod
    def register(cls):
        bpy.types.Object.blendals_midi_track = bpy.props.PointerProperty(
            name="Blendals MIDI Track",
            description="Blendals MIDI Track Properties",
            type=cls,
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Object.blendals_midi_track


class BLENDALS_OT_ApplyAnimation(bpy.types.Operator):
    bl_idname = "blendals.apply_animation"
    bl_label = "Apply Animation"

    @classmethod
    def poll(cls, context):
        return is_midi_track_object(context.object)

    def execute(self, context: bpy_types.Context) -> set[str]:
        self.report({"INFO"}, f"444")
        print(context.object.blendals_midi_track.midi_track)
        return {'FINISHED'}


class BLENDALS_PT_MidiTrackInfo(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Blendals MIDI Track Info"
    bl_idname = "OBJECT_PT_blendals_midi_track_info"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context) -> bool:
        return is_midi_track_object(context.object)

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text=f"Track ID: {obj.blendals_midi_track.track_id}")
        row = layout.row()
        row.label(text=f"Notes number: {obj.blendals_midi_track.notes_number}")
        row = layout.row()
        row.operator(BLENDALS_OT_ApplyAnimation.bl_idname)


def is_midi_track_object(obj: bpy_types.Object | None) -> bool:
    if obj is None:
        return False
    return bool(obj.blendals_midi_track.track_id)
