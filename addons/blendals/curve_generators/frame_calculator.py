import logging

logger = logging.Logger(__name__)


class FrameCalculator:

    def __init__(
        self,
        song_bpm: int,
        song_bar_start: int,
        song_time_signature_numerator: int,
        video_fps: int,
        video_frame_start: int,
    ):
        beats_per_seconds = song_bpm / 60
        self._frames_per_beat = video_fps / beats_per_seconds
        start_beats_offset = (song_bar_start - 1) * song_time_signature_numerator
        self.start_frame = video_frame_start - start_beats_offset * self._frames_per_beat
        if self.start_frame % 1 != 0:
            logger.warning("start_frame is not integer: %s", self.start_frame)
        self.start_frame = int(self.start_frame)

    def beat_to_frame(self, beat: float) -> int:
        return int(self.start_frame + beat * self._frames_per_beat)
