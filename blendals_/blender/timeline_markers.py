import bpy

from blendals_.config import settings
from blendals_.frame_calculator import frame_calculator


def add_timeline_markers_for_bars(bars_number=10) -> None:
    clear_bars_markers()

    for i in range(bars_number):
        current_bar = settings.SONG_START_BAR + i - 1
        if current_bar <= 1:
            current_bar = 1

        beat = (current_bar - 1) * settings.SONG_BAR_SIZE_BEATS
        frame = frame_calculator.beat_to_frame(beat)
        bpy.context.scene.timeline_markers.new(name=str(current_bar), frame=frame)


def clear_bars_markers() -> None:
    bpy.context.scene.timeline_markers.clear()
