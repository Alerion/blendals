import json

import dacite

import bpy
import bpy_types

from blendals.data.song import MidiTrack, Note
from blendals.blnder_utils.enums import PropertySubtypeNumber, WMReport, OperatorReturn, OperatorTypeFlag, FModifierType
from blendals.curve_generators.frame_calculator import FrameCalculator
from blendals.curve_generators.curve_manipulations import set_keyframe_point

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
        midi_track_data = json.loads(self.raw_data)
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
    bl_label = "Apply Scale Animation"
    bl_options = {OperatorTypeFlag.REGISTER}

    max_scale: bpy.props.FloatProperty(
        name="Max Scale",
        default=1,
        soft_min=0,
        soft_max=10,
    )
    sustain_scale: bpy.props.FloatProperty(
        name="Sustain Scale",
        default=0.75,
        soft_min=0,
        soft_max=10,
    )
    attack: bpy.props.FloatProperty(
        name="Attack",
        description="Value is a fraction of a note length",
        default=0.25,
        min=0,
        soft_max=1,
        subtype=PropertySubtypeNumber.FACTOR,
    )
    decay: bpy.props.FloatProperty(
        name="Decay",
        description="Value is a fraction of a note length",
        default=0.25,
        min=0,
        soft_max=1,
        subtype=PropertySubtypeNumber.FACTOR,
    )
    release: bpy.props.FloatProperty(
        name="Release",
        description="Value is a fraction of a note length",
        default=0.5,
        min=0,
        soft_max=1,
        subtype=PropertySubtypeNumber.FACTOR,
    )
    loop: bpy.props.BoolProperty(
        name="Loop",
        description="Add Cycles F-Modifier to generated F-Curve",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return is_midi_track_object(context.object)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context: bpy_types.Context) -> set[OperatorReturn]:
        midi_track_object = context.object

        if midi_track_object.animation_data is None:
            self.report({WMReport.WARNING}, "Object does not have animation data.")
            return {OperatorReturn.CANCELLED}

        song_obj = midi_track_object.parent
        frame_calculator = FrameCalculator.create_from_song(song_obj, context.scene)
        midi_track: MidiTrack = midi_track_object.blendals_midi_track.midi_track
        midi_track_object.animation_data.action = bpy.data.actions.new(name=f"Scale by MIDI: {midi_track.id}")

        for scale_index in range(3):
            animation_curve = midi_track_object.animation_data.action.fcurves.new(
                data_path="scale", index=scale_index
            )

            self._add_boundaries_keyframes(frame_calculator, animation_curve, song_obj)

            for note in midi_track.notes:
                self._add_note_to_animation_curve(frame_calculator, animation_curve, note)

            if self.loop:
                animation_curve.modifiers.new(type=FModifierType.CYCLES)

        return {OperatorReturn.FINISHED}

    def _add_note_to_animation_curve(self, frame_calculator: FrameCalculator, animation_curve: bpy.types.FCurve, note: Note) -> None:
        note_start_frame = frame_calculator.beat_to_frame(note.start)
        note_end_frame = frame_calculator.beat_to_frame(note.end)

        _note_length_in_frames = note_end_frame - note_start_frame
        peak_frame = note_start_frame + _note_length_in_frames * max(self.attack, 0.001)
        sustain_start_frame = note_start_frame + _note_length_in_frames * (self.attack + self.decay)
        release_end_frame = note_end_frame + _note_length_in_frames * max(self.release, 0.001)

        print(note_start_frame, peak_frame, sustain_start_frame, note_end_frame, release_end_frame)

        set_keyframe_point(animation_curve, frame=note_start_frame, value=0)
        set_keyframe_point(animation_curve, frame=peak_frame, value=self.max_scale)

        if sustain_start_frame != peak_frame:
            set_keyframe_point(animation_curve, frame=sustain_start_frame, value=self.sustain_scale)

        set_keyframe_point(animation_curve, frame=note_end_frame, value=self.sustain_scale)
        set_keyframe_point(animation_curve, frame=release_end_frame, value=0)

    def _add_boundaries_keyframes(self, frame_calculator: FrameCalculator, animation_curve: bpy.types.FCurve,
                                  song_obj: bpy_types.Object) -> None:
        # Add first frame.
        set_keyframe_point(animation_curve, frame=frame_calculator.start_frame, value=0)
        # Add last frame.
        final_beat = song_obj.blendals_song.length_in_bars * song_obj.blendals_song.time_signature_numerator
        frame = frame_calculator.beat_to_frame(final_beat)
        set_keyframe_point(animation_curve, frame=frame, value=0)


class BLENDALS_PT_MidiTrackInfo(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Blendals MIDI Track Info"
    bl_idname = "OBJECT_PT_blendals_midi_track_info"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        return is_midi_track_object(context.object)

    def draw(self, context: bpy_types.Context):
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
