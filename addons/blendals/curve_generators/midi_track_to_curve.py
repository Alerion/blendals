from bpy.types import FCurve

from blendals.curve_generators.curve_manipulations import set_keyframe_point
from blendals.song import MidiTrack, Note
from blendals.frame_calculator import frame_calculator


class MidiTrackToCurve:

    def __init__(
        self,
        midi_track: MidiTrack,
        *,
        min_value: float = 0,
        value_range: float = 1,
        note_attack: float = 0.25,
        note_release: float = 1,
    ):
        self.min_value = min_value
        self.value_range = value_range
        # From 0 to 1 value. When animation reach max value withing a note length.
        self.note_attack = note_attack
        self.note_release = note_release
        self.track: MidiTrack = midi_track
        self.name = self.track.id

    def apply_track_to_curve(self, animation_curve: FCurve) -> None:
        for note in self.track.notes:
            self._add_note_to_animation_curve(animation_curve, note)

    def _add_note_to_animation_curve(self, animation_curve: FCurve, note: Note) -> None:
        start_frame = frame_calculator.beat_to_frame(note.start)
        end_frame = frame_calculator.beat_to_frame(note.end)

        peak_frame = start_frame + (end_frame - start_frame) * self.note_attack
        end_frame = start_frame + (end_frame - start_frame) * self.note_release

        set_keyframe_point(animation_curve, frame=start_frame, value=self.min_value)
        set_keyframe_point(animation_curve, frame=peak_frame, value=self.min_value + self.value_range)
        set_keyframe_point(animation_curve, frame=end_frame, value=self.min_value)


