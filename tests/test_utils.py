# -*- coding: utf-8 -*-

from audinota.utils import (
    segment_audio_by_count,
    get_audio_duration,
    segment_audio_by_duration,
)

from audinota.tests.audio_files import AudioFileEnum


def test_segment_audio_by_count():
    for audio_file in AudioFileEnum.iter():
        segments = segment_audio_by_count(
            audio=audio_file.audio,
            n_seg=4,
        )
        assert len(segments) == 4


def test_get_audio_duration():
    cases = [
        (AudioFileEnum.a01_ai_karen_hao_agi_openai_ai_10min, (10, 11)),
        (AudioFileEnum.a02_stablecoin_15min, (15, 16)),
        (AudioFileEnum.a03_luo_ji_si_wei_kai_hui_60min, (58, 59)),
    ]
    for audio_file, (lower, upper) in cases:
        duration = get_audio_duration(audio_file.audio)
        assert (lower * 60) <= duration <= (upper * 60)


def test_segment_audio_by_duration():
    cases = [
        (AudioFileEnum.a01_ai_karen_hao_agi_openai_ai_10min, 11),
        (AudioFileEnum.a02_stablecoin_15min, 16),
        (AudioFileEnum.a03_luo_ji_si_wei_kai_hui_60min, 59),
    ]
    for audio_file, n in cases:
        segments = segment_audio_by_duration(
            audio=audio_file.audio,
            duration=60,  # seconds
        )
        assert len(segments) == n


if __name__ == "__main__":
    from audinota.tests import run_cov_test

    run_cov_test(
        __file__,
        "audinota.utils",
        preview=False,
    )
