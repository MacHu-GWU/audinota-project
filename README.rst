
.. image:: https://readthedocs.org/projects/audinota/badge/?version=latest
    :target: https://audinota.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/audinota-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/audinota-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/audinota-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/audinota-project

.. image:: https://img.shields.io/pypi/v/audinota.svg
    :target: https://pypi.python.org/pypi/audinota

.. image:: https://img.shields.io/pypi/l/audinota.svg
    :target: https://pypi.python.org/pypi/audinota

.. image:: https://img.shields.io/pypi/pyversions/audinota.svg
    :target: https://pypi.python.org/pypi/audinota

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/audinota-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/audinota-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://audinota.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/audinota-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/audinota-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/audinota-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/audinota#files


Welcome to ``audinota`` Documentation
==============================================================================
.. image:: https://audinota.readthedocs.io/en/latest/_static/audinota-logo.png
    :target: https://audinota.readthedocs.io/en/latest/

**Audinota** (Latin for "taking notes from audio") is a lightweight, high-performance Python library designed for fast audio-to-text transcription. Built specifically for extracting textual information from audio content, Audinota enables you to leverage AI-powered text analysis, summarization, and processing on your audio data.

The library is built on top of the proven faster-whisper open-source framework and features intelligent automatic audio segmentation with parallel processing capabilities. By automatically chunking large audio files and utilizing multiple CPU cores, Audinota delivers exceptional transcription speed while maintaining accuracy.

Audinota follows a "deadly simple" philosophy - it focuses exclusively on pure audio-to-text conversion without the complexity of subtitle generation or timestamp management. This streamlined approach makes it ideal for information-dense audio content such as research videos, podcasts, lectures, and educational materials.

The project was inspired by real-world research workflows where rapid consumption and analysis of valuable audio content from YouTube videos, podcasts, and other sources is essential. Whether you're a researcher, content creator, or data analyst, Audinota helps you quickly transform audio insights into actionable text for further AI-powered processing and analysis.


Quick Start
------------------------------------------------------------------------------
Audinota makes audio transcription incredibly simple with just a few lines of code:

.. code-block:: python

    import io
    from pathlib import Path
    from audinota.api import transcribe_audio_in_parallel

    # Transcribe any audio file to text
    text = transcribe_audio_in_parallel(
        audio=io.BytesIO(Path("podcast_episode.mp3").read_bytes()),
    )
    print(text)

**What happens under the hood:**

1. **Automatic Format Detection**: Audinota automatically handles popular audio formats including MP3, MP4, WAV, M4A, FLAC, OGG, and more
2. **Language Detection**: The system automatically detects the spoken language without requiring manual specification
3. **Smart Segmentation**: Large audio files are intelligently chunked into optimal segments for processing
4. **Parallel Processing**: Multiple CPU cores work simultaneously on different audio segments for maximum speed
5. **Text Assembly**: All transcribed segments are seamlessly combined into a single, coherent text output

The entire process is optimized for speed and accuracy, typically processing hours of audio content in just minutes while maintaining high transcription quality across different languages and audio conditions.


.. _install:

Install
------------------------------------------------------------------------------

``audinota`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install audinota

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade audinota
