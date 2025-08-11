
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

**💰 Massive Cost Savings**: While AWS Transcribe costs $0.024/minute ($1.44/hour), Audinota can be deployed on AWS Lambda for approximately $0.0002/minute - making it **120x cheaper** than commercial transcription services. This dramatic cost reduction enables researchers, content creators, and businesses to extract valuable insights from extensive audio archives and YouTube content libraries without breaking the budget. Transform hours of audio content into actionable text for AI analysis, knowledge extraction, and content research at a fraction of traditional cloud service costs.


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


Command Line Interface
------------------------------------------------------------------------------
Audinota provides a powerful command-line interface for easy audio transcription without writing code:

Basic Usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: console

    # Simple transcription - output saved next to input file
    $ audinota transcribe --input="podcast.mp3"

    # Specify output directory
    $ audinota transcribe --input="lecture.mp4" --output="/path/to/transcripts/"

    # Specify exact output file
    $ audinota transcribe --input="interview.wav" --output="result.txt"

    # Overwrite existing files
    $ audinota transcribe --input="audio.m4a" --output="existing.txt" --overwrite

Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**--input** (required)
    Path to the input audio file. Supports popular formats including:
    
    - MP3, MP4, M4A (most common)
    - WAV, FLAC, OGG (uncompressed/lossless)
    - And many more formats supported by faster-whisper

**--output** (optional)
    Controls where the transcription is saved:

    - **Not specified**: Creates a .txt file next to the input file
      
      .. code-block:: console
      
          $ audinota transcribe --input="podcast.mp3"
          # Creates: podcast.txt

    - **Directory path**: Creates a .txt file in the specified directory
      
      .. code-block:: console
      
          $ audinota transcribe --input="podcast.mp3" --output="/transcripts/"
          # Creates: /transcripts/podcast.txt

    - **File path**: Uses the exact specified file path
      
      .. code-block:: console
      
          $ audinota transcribe --input="podcast.mp3" --output="my_transcript.txt"
          # Creates: my_transcript.txt

**--overwrite** (optional, default: False)
    Boolean flag that controls file overwriting behavior:

    - **False** (default): If output file exists, shows error and stops
    - **True**: Overwrites existing output files without asking

    .. note::
        This only applies when --output specifies a file path. Directory outputs use automatic numbering instead.

File Conflict Resolution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Audinota intelligently handles file name conflicts:

**Automatic Numbering**
    When output goes to a directory and files already exist:

    .. code-block:: console

        $ audinota transcribe --input="audio.mp3" --output="/transcripts/"
        # If /transcripts/audio.txt exists, creates /transcripts/audio_01.txt
        # If both exist, creates /transcripts/audio_02.txt, etc.

**File Path Conflicts**
    When --output specifies an existing file:

    .. code-block:: console

        $ audinota transcribe --input="audio.mp3" --output="existing.txt"
        # Error: Output file 'existing.txt' already exists. Use --overwrite

        $ audinota transcribe --input="audio.mp3" --output="existing.txt" --overwrite
        # Overwrites existing.txt

Real-World Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: console

    # Transcribe a podcast episode
    $ audinota transcribe --input="episode_042.mp3"
    # Output: episode_042.txt

    # Batch processing to organized directory
    $ mkdir transcripts
    $ audinota transcribe --input="meeting_2024_01.m4a" --output="transcripts/"
    $ audinota transcribe --input="meeting_2024_02.m4a" --output="transcripts/"
    # Output: transcripts/meeting_2024_01.txt, transcripts/meeting_2024_02.txt

    # Process lecture with custom naming
    $ audinota transcribe --input="cs101_lecture.mp4" --output="notes/week1_lecture.txt"

    # Replace previous transcription
    $ audinota transcribe --input="revised_audio.wav" --output="final_transcript.txt" --overwrite

Performance Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The CLI automatically provides:

- **🚀Parallel Processing**: Utilizes all CPU cores for maximum speed
- **🧠Smart Segmentation**: Automatically splits large files for optimal processing
- **🌍Language Detection**: Automatically detects spoken language
- **📊Progress Feedback**: Real-time status updates with emoji indicators
- **🔍Format Detection**: Handles various audio formats without configuration

.. code-block:: console

    $ audinota transcribe --input="long_podcast.mp3"
    🎵 Transcribing audio file: long_podcast.mp3
    📝 Output will be saved to: long_podcast.txt
    🔄 Loading audio data...
    🚀 Starting parallel transcription...
    💾 Saving transcription...
    ✅ Transcription completed successfully!
    📄 Output saved to: file:///path/to/long_podcast.txt
    📊 Text length: 15,847 characters


.. _install:

Install
------------------------------------------------------------------------------

``audinota`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install audinota

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade audinota
