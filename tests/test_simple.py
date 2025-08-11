# -*- coding: utf-8 -*-

from audinota.utils import segment_audio

import io

from audinota.tests.audio_files import AudioFileEnum


def test_segment_audio():
    for audio_file in AudioFileEnum.iter():
        audio = io.BytesIO(audio_file.read())
        segments = segment_audio(
            audio=audio,
            n_seg=4,
        )
        assert len(segments) == 4


if __name__ == "__main__":
    from audinota.tests import run_cov_test

    run_cov_test(
        __file__,
        "audinota.utils",
        preview=False,
    )
