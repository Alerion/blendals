import bpy
from bpy.types import Keyframe, FCurveKeyframePoints, FCurve
from bpy_types import Object
from rich import print

from blendals.live_set_to_song import Track, Song, Note
from blendals.blender.enums import KeyframeTransition, KeyframeHandleType
from blendals.config import settings


class ScaleControlAnimationGenerator:
    # TODO: Scale with velocity

    def __init__(self, *, min_scale: float = 1, max_scale: float = 2, note_attack: float = 0.25, note_release: float = 1):
        self.min_scale = min_scale
        self.max_scale = max_scale
        # From 0 to 1 value. When animation reach max value withing a note length.
        self.note_attack = note_attack
        self.note_release = note_release

        self.interpolation = KeyframeTransition.LINEAR
        self.handle_frame_distance = 1

        self._frame_calculator: FrameCalculator
        self._track: Track

    def init(self, track: Track, song: Song) -> None:
        print(f"Init {self.__class__.__name__} for {track.id}")
        self._frame_calculator = FrameCalculator(song.tempo)
        self._track = track

    def generate(self, control: Object) -> None:
        print(f"Generate {self.__class__.__name__} animation for {self._track.id}")
        control.animation_data_clear()
        control.animation_data_create()
        control.animation_data.action = bpy.data.actions.new(name=f"{self._track.id} Scale Animation")
        # Generate animation for all three scale dimensions
        for scale_index in range(3):
            animation_curve = control.animation_data.action.fcurves.new(data_path="scale", index=scale_index)
            for note in self._track.notes:
                self._add_note_to_animation_curve(animation_curve, note)

    def _add_note_to_animation_curve(self, animation_curve: FCurve, note: Note) -> None:
        start_frame = self._frame_calculator.beat_to_frame(note.start)
        end_frame = self._frame_calculator.beat_to_frame(note.end)

        peak_frame = start_frame + (end_frame - start_frame) * self.note_attack
        end_frame = start_frame + (end_frame - start_frame) * self.note_release

        self._set_keyframe_point(animation_curve, frame=start_frame, value=self.min_scale)
        self._set_keyframe_point(animation_curve, frame=peak_frame, value=self.max_scale)
        self._set_keyframe_point(animation_curve, frame=end_frame, value=self.min_scale)

    def _set_keyframe_point(self, animation_curve: FCurve, frame: float, value: float) -> None:
        keyframe_points: FCurveKeyframePoints = animation_curve.keyframe_points
        keyframe_point = keyframe_points.insert(frame, value)

        keyframe_point.interpolation = self.interpolation
        if self.interpolation == KeyframeTransition.BEZIER:
            keyframe_point.handle_left_type = KeyframeHandleType.AUTO
            keyframe_point.handle_left = (frame - self.handle_frame_distance, value)
            keyframe_point.handle_right_type = KeyframeHandleType.AUTO
            keyframe_point.handle_right = (frame + self.handle_frame_distance, value)


class FrameCalculator:

    def __init__(self, song_tempo: int, frame_rate: int = settings.FRAME_RATE_FPS, start_frame: int = settings.START_FRAME):
        self.song_tempo = song_tempo
        self.beats_per_seconds = song_tempo / 60
        self.frame_rate = frame_rate
        self.start_frame = start_frame

    def beat_to_frame(self, beat: float) -> float:
        return self.start_frame + beat * self.frame_rate / self.beats_per_seconds
