# -*- coding: utf-8 -*-

import typing as T
import io
import dataclasses

import mpire
from faster_whisper import WhisperModel, BatchedInferencePipeline
from faster_whisper.transcribe import TranscriptionInfo, Segment

from .utils import segment_audio_by_duration


@dataclasses.dataclass
class TranscribeAudioResult:
    text: str = dataclasses.field()
    segments: list[Segment] = dataclasses.field()
    info: TranscriptionInfo = dataclasses.field()


def transcribe_audio(
    audio: T.BinaryIO,
    whisper_model_kwargs: dict[str, T.Any],
    transcribe_kwargs: dict[str, T.Any],
) -> TranscribeAudioResult:
    model = WhisperModel(**whisper_model_kwargs)
    # Wrapper for batched inference - processes multiple audio segments in parallel for better throughput
    batched_infer_pipeline = BatchedInferencePipeline(model=model)
    segments, info = batched_infer_pipeline.transcribe(
        audio=audio,
        **transcribe_kwargs,
    )
    segments = list(segments)
    text = "".join([segment.text for segment in segments])
    return TranscribeAudioResult(
        text=text,
        segments=segments,
        info=info,
    )


def transcribe_audio_in_parallel(
    audio: T.BinaryIO,
    seg_duration: int = 120,
    n_jobs: T.Optional[int] = None,
) -> str:
    """
    Transcribe audio in parallel by splitting it into segments of specified duration.

    :param audio: Audio data as a binary stream. Usually from ``io.BytesIO(Path("...").read_bytes())``.
    :param seg_duration: Duration of each segment in seconds. Default is 120 seconds.
    :param n_jobs: Number of parallel jobs to run. If None, uses all available CPU cores.

    :return: Transcribed text from the audio.
    """
    segments = segment_audio_by_duration(audio=audio, duration=seg_duration)
    tasks = list()
    for segment in segments:
        whisper_model_kwargs = dict(
            # Model size or path - "tiny", "base", "small", "medium", "large-v2" or a custom model path
            model_size_or_path="tiny",
            # CPU only
            device="cpu",
            # int 8 quantization for faster inference
            compute_type="int8",
            cpu_threads=1,
            # cpu_threads=8,
            num_workers=1,
        )
        transcribe_kwargs = dict(
            # Maximum number of parallel decoding requests - higher values increase throughput but use more memory
            batch_size=16,
            # Language code (e.g., "en", "zh", "ja") or None for automatic detection
            language=None,
            # Task type: "transcribe" for speech-to-text or "translate" for speech-to-english translation
            task="transcribe",
            # Enable Voice Activity Detection to filter out non-speech segments (default True for BatchedInferencePipeline)
            vad_filter=True,
            vad_parameters=dict(
                # Silero VAD configuration: minimum silence duration to split audio
                min_silence_duration_ms=500
            ),
        )
        task = {
            "audio": io.BytesIO(segment),
            "whisper_model_kwargs": whisper_model_kwargs,
            "transcribe_kwargs": transcribe_kwargs,
        }
        tasks.append(task)

    with mpire.WorkerPool(
        n_jobs=n_jobs,
        start_method="spawn",
    ) as pool:
        results = pool.map(
            transcribe_audio,
            tasks,
        )
        text = "".join([result.text for result in results])

    return text
