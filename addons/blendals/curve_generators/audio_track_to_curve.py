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
        audio_track: AudioTrack,
        *,
        min_value: float = 1,
        max_value: float = 2,
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.track: AudioTrack = audio_track
        self.name = self.track.id

    def apply_track_to_curve(self, animation_curve: FCurve) -> None:
        for point in self.track.points:
            self._add_point_to_animation_curve(animation_curve, point)

    def _add_point_to_animation_curve(self, animation_curve: FCurve, point: Point):
        frame = frame_calculator.beat_to_frame(point.time)
        frame_value = self.min_value + (self.max_value - self.min_value) * point.value
        set_keyframe_point(animation_curve, frame=frame, value=frame_value)
