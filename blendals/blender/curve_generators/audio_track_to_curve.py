from bpy.types import Keyframe, FCurveKeyframePoints, FCurve
from bpy_types import Object
from rich import print

from blendals.song import MidiTrack, AudioTrack, Point
from blendals.blender.enums import KeyframeTransition, KeyframeHandleType
from blendals.frame_calculator import frame_calculator
from blendals.blender.curve_generators.curve_manipulations import set_keyframe_point


class AudioTrackToCurve:

    def __init__(
        self,
        *,
        min_value: float = 1,
        max_value: float = 2,
    ):
        self.min_value = min_value
        self.max_value = max_value

    def apply_track_to_curve(self, animation_curve: FCurve, audio_track: AudioTrack) -> None:
        for point in audio_track.points:
            self._add_point_to_animation_curve(animation_curve, point)

    def _add_point_to_animation_curve(self, animation_curve: FCurve, point: Point):
        frame = frame_calculator.beat_to_frame(point.time)
        frame_value = self.min_value + (self.max_value - self.min_value) * point.value
        set_keyframe_point(animation_curve, frame=frame, value=frame_value)
