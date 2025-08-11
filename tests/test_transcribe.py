# -*- coding: utf-8 -*-

from audinota.transcribe import transcribe_audio_in_parallel
from audinota.tests.audio_files import AudioFileEnum


def get_whisper_model_kwargs():
    return dict(
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


def get_transcribe_kwargs():
    return dict(
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


def test_transcribe_audio_in_parallel():
    # fmt: off
    text = transcribe_audio_in_parallel(audio=AudioFileEnum.a01_ai_karen_hao_agi_openai_ai_10min.audio)
    # text = transcribe_audio_in_parallel(audio=AudioFileEnum.a02_stablecoin_15min.audio)
    # text = transcribe_audio_in_parallel(audio=AudioFileEnum.a03_luo_ji_si_wei_kai_hui_60min.audio)
    # fmt: on
    # print(text) # for debug only


if __name__ == "__main__":
    from audinota.tests import run_cov_test

    run_cov_test(
        __file__,
        "audinota.transcribe",
        preview=False,
    )
