import math
from pathlib import Path

import soundfile as sf
import numpy as np

from blendals.live_set import AudioChannelPoint


def extract_points_from_audio_file(
    audio_file_path: Path, bpm: int
) -> tuple[list[AudioChannelPoint], list[AudioChannelPoint]]:
    audio_file = sf.SoundFile(audio_file_path)
    signal_array = audio_file.read()
    left_channel = signal_array[:, 0]
    right_channel = signal_array[:, 1]
    return (
        get_audio_points_from_audio_data(audio_file, left_channel, bpm),
        get_audio_points_from_audio_data(audio_file, right_channel, bpm),
    )


def get_audio_points_from_audio_data(
    audio_file: sf.SoundFile, audio_data: np.ndarray, bpm: int
) -> list[AudioChannelPoint]:
    audio_length = audio_file.frames / audio_file.samplerate
    resample_ratio = audio_file.samplerate / 1000
    kernel = get_ones_kernel(kernel_size=35)
    # Increase to reduce number of points in output
    final_resample_ratio = 25
    convolved_l_channel_35 = smooth_audio_data(
        audio_data, resample_ratio, kernel, final_resample_ratio
    )
    times = np.linspace(0, audio_length, num=convolved_l_channel_35.shape[0])
    # Convert seconds to audio track beats
    times = times / bpm * 60

    output = []
    for time, value in zip(times, convolved_l_channel_35):
        output.append(AudioChannelPoint(time=float(time), value=float(value)))
    return output


def smooth_audio_data(
    audio_data: np.ndarray,
    resample_ratio: float,
    kernel: np.ndarray,
    final_resample_ratio: int,
):
    absolute_audio_data = np.absolute(audio_data)
    resampled_audio_data = np.interp(
        np.arange(0, len(absolute_audio_data), resample_ratio),
        np.arange(0, len(absolute_audio_data)),
        absolute_audio_data,
    )
    convolved_data = np.convolve(resampled_audio_data, kernel, mode="same")

    resampled_convolved_data = np.interp(
        np.arange(0, len(convolved_data), final_resample_ratio),
        np.arange(0, len(convolved_data)),
        convolved_data,
    )

    return normalize_between_0_and_1(resampled_convolved_data)


def get_quadratic_kernel(kernel_size):
    """
    After output normalisation it is almost equal to the ones kernel.
    """
    kernel = np.array(range(kernel_size))
    kernel = kernel - math.floor(kernel_size / 2)
    kernel = kernel / kernel_size
    kernel = np.ma.power(kernel, 2)
    kernel = kernel * -1
    kernel = kernel + abs(np.ma.min(kernel))
    return kernel


def get_ones_kernel(kernel_size):
    return np.ones(kernel_size) / kernel_size


def normalize_between_0_and_1(audio_data: np.ndarray) -> np.ndarray:
    return (audio_data - np.min(audio_data)) / (np.max(audio_data) - np.min(audio_data))
