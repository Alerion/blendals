from typing import Union

import bpy
from bpy.types import Keyframe, FCurveKeyframePoints, FCurve
from bpy_types import Object
from rich import print

from blendals.song import MidiTrack, AudioTrack, Note
from blendals.blender.enums import KeyframeTransition, KeyframeHandleType
from blendals.frame_calculator import frame_calculator


class ScaleAnimation:
    # TODO: Scale with velocity

    def __init__(self, curve_generator):
        self._curve_generator = curve_generator

    def generate(self, control: Object, track: Union[MidiTrack, AudioTrack]) -> None:
        print(f"Generate {self.__class__.__name__} animation for {track.id}")
        control.animation_data_clear()
        control.animation_data_create()
        control.animation_data.action = bpy.data.actions.new(
            name=f"{track.id} Scale Animation"
        )
        # Generate animation for all three scale dimensions
        for scale_index in range(3):
            animation_curve = control.animation_data.action.fcurves.new(
                data_path="scale", index=scale_index
            )
            self._curve_generator.apply_track_to_curve(animation_curve, track)
