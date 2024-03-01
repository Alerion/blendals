import logging

from blendals_.config import settings, Settings

logger = logging.Logger(__name__)


class FrameCalculator:

    def __init__(self, project_settings: Settings):
        beats_per_seconds = project_settings.SONG_TEMPO / 60
        self._frames_per_beat = project_settings.FRAME_RATE_FPS / beats_per_seconds
        start_beats_offset = (project_settings.SONG_START_BAR - 1) * project_settings.SONG_BAR_SIZE_BEATS
        self.start_frame = project_settings.FIRST_VIDEO_FRAME - start_beats_offset * self._frames_per_beat
        if self.start_frame % 1 != 0:
            logger.warning("start_frame is not integer: %s", self.start_frame)
        self.start_frame = int(self.start_frame)

    def beat_to_frame(self, beat: float) -> int:
        return int(self.start_frame + beat * self._frames_per_beat)


frame_calculator = FrameCalculator(settings)
