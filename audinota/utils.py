# -*- coding: utf-8 -*-

import typing as T
import io

import librosa
import soundfile


def segment_audio(
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

    # Load audio data using librosa
    y, sr = librosa.load(audio, sr=None)

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
