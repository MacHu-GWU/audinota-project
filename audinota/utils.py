# -*- coding: utf-8 -*-

"""
Audio Processing Utilities

This module provides utilities for audio segmentation and metadata extraction.
It uses soundfile for direct audio I/O to avoid deprecated audioread dependencies.
"""

import typing as T
import io
import math

import soundfile


def segment_audio_by_count(
    audio: T.BinaryIO,
    n_seg: int,
) -> list[bytes]:
    """
    Split audio into a fixed number of segments with equal duration.
    
    Each segment will have approximately the same duration, with the last segment
    potentially being slightly longer to include any remaining samples.
    
    :param audio: Audio data as a binary stream (e.g., io.BytesIO from file bytes)
    :param n_seg: Number of segments to create (must be positive integer)
    
    :return: List of WAV audio segments as bytes, ready for further processing
    
    Example:
        >>> audio_bytes = Path("audio.mp3").read_bytes()
        >>> audio_stream = io.BytesIO(audio_bytes)
        >>> segments = segment_audio_by_count(audio_stream, 4)
        >>> print(f"Created {len(segments)} segments")
    """
    # Reset stream to beginning to ensure we read from start
    audio.seek(0)

    # Load audio data directly with soundfile (avoids deprecated audioread)
    audio_data, sample_rate = soundfile.read(audio)

    # Calculate samples per segment for equal distribution
    total_samples = len(audio_data)
    samples_per_segment = total_samples // n_seg

    segments = []

    # Create segments with equal sample counts
    for segment_idx in range(n_seg):
        # Calculate segment boundaries in sample indices
        start_sample = segment_idx * samples_per_segment
        
        # Last segment includes any remaining samples to avoid data loss
        if segment_idx == n_seg - 1:
            end_sample = total_samples
        else:
            end_sample = (segment_idx + 1) * samples_per_segment

        # Extract audio data for this segment
        segment_audio_data = audio_data[start_sample:end_sample]

        # Convert segment to WAV bytes for compatibility
        segment_buffer = io.BytesIO()
        soundfile.write(segment_buffer, segment_audio_data, sample_rate, format="WAV")
        segment_buffer.seek(0)

        # Store the complete WAV file as bytes
        segments.append(segment_buffer.getvalue())

    return segments


def get_audio_duration(audio: T.BinaryIO) -> float:
    """
    Get audio duration in seconds from audio metadata without loading audio data.
    
    This function reads only the audio file header to extract duration information,
    making it efficient for large audio files where you only need the duration.
    
    :param audio: Audio data as a binary stream (e.g., io.BytesIO from file bytes)
    
    :return: Audio duration in seconds as a floating-point number
    
    Example:
        >>> audio_bytes = Path("recording.wav").read_bytes()
        >>> audio_stream = io.BytesIO(audio_bytes)
        >>> duration = get_audio_duration(audio_stream)
        >>> print(f"Audio is {duration:.1f} seconds long")
    """
    # Reset stream to beginning for reliable metadata reading
    audio.seek(0)
    
    # Extract audio metadata efficiently (header-only, no data loading)
    audio_info = soundfile.info(audio)
    
    # Reset stream position for subsequent operations
    audio.seek(0)
    
    return audio_info.duration


def segment_audio_by_duration(
    audio: T.BinaryIO,
    duration: float,
) -> list[bytes]:
    """
    Split audio into segments with a target duration per segment.
    
    The audio will be divided into segments where each segment (except possibly
    the last one) has approximately the specified duration. The last segment
    may be shorter if the total duration is not evenly divisible.
    
    :param audio: Audio data as a binary stream (e.g., io.BytesIO from file bytes)
    :param duration: Target duration for each segment in seconds (can be fractional)
    
    :return: List of WAV audio segments as bytes, ready for further processing
    
    Example:
        >>> audio_bytes = Path("lecture.mp3").read_bytes()
        >>> audio_stream = io.BytesIO(audio_bytes)
        >>> # Split into 2-minute segments
        >>> segments = segment_audio_by_duration(audio_stream, 120.0)
        >>> print(f"Created {len(segments)} segments of ~2 minutes each")
    """
    # Get total audio duration from metadata
    total_duration = get_audio_duration(audio)
    
    # Calculate number of segments needed to achieve target duration
    num_segments = math.ceil(total_duration / duration)
    
    # Delegate to count-based segmentation for consistent behavior
    return segment_audio_by_count(audio, num_segments)
