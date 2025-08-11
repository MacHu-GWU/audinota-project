# -*- coding: utf-8 -*-

import typing as T
import io
import math

import soundfile


def segment_audio_by_count(
    audio: T.BinaryIO,
    n_seg: int,
) -> list[bytes]:
    """
    Segment audio data into `n_seg` parts.

    :param audio: Audio data as a binary stream. Usually from ``io.BytesIO(Path("...").read_bytes())``.
    :param n_seg: Number of segments to split the audio into.

    :return: List of audio segments as bytes.
    """
    # Reset stream position to beginning
    audio.seek(0)

    # Read audio data using soundfile directly (avoids audioread deprecation warnings)
    y, sr = soundfile.read(audio)

    # Calculate segment length in samples
    total_samples = len(y)
    segment_samples = total_samples // n_seg

    segments = []

    for i in range(n_seg):
        start_sample = i * segment_samples

        # For the last segment, include all remaining samples
        if i == n_seg - 1:
            end_sample = total_samples
        else:
            end_sample = (i + 1) * segment_samples

        # Extract segment
        segment_data = y[start_sample:end_sample]

        # Convert segment to bytes using soundfile
        segment_bytes = io.BytesIO()
        soundfile.write(segment_bytes, segment_data, sr, format="WAV")
        segment_bytes.seek(0)

        # Get the bytes content
        segments.append(segment_bytes.getvalue())

    return segments


def get_audio_duration(audio: T.BinaryIO) -> float:
    """
    Get audio duration in seconds without loading the entire file.

    :param audio: Audio data as BytesIO
    :return: Duration in seconds
    """
    audio.seek(0)  # Reset to beginning
    info = soundfile.info(audio)
    audio.seek(0)  # Reset again for future use
    return info.duration


def segment_audio_by_duration(
    audio: T.BinaryIO,
    duration: int,
) -> list[bytes]:
    """
    Segment audio data into parts of specified duration.

    :param audio: Audio data as a binary stream. Usually from ``io.BytesIO(Path("...").read_bytes())``.
    :param duration: Duration of each segment in seconds.

    :return: List of audio segments as bytes.
    """
    total_duration = get_audio_duration(audio)
    n_seg = math.ceil(total_duration / duration)
    return segment_audio_by_count(audio, n_seg)
