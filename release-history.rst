.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.1 (2024-08-11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- **Core Transcription Engine**: Built on faster-whisper for high-accuracy audio-to-text conversion
- **Parallel Processing**: Automatic audio segmentation with multi-CPU core processing for exceptional speed
- **Smart Audio Segmentation**: Intelligent chunking of large audio files by duration or segment count
- **Multi-Format Support**: Handles popular audio formats including MP3, MP4, WAV, M4A, FLAC, OGG
- **Automatic Language Detection**: AI-powered language detection without manual specification
- **Command Line Interface**: Simple CLI with `audinota transcribe --input="file.mp3"` syntax
- **Flexible Output Management**: Support for directory output, custom file naming, and automatic conflict resolution
- **Cost-Effective Solution**: 120x cheaper than AWS Transcribe when deployed on cloud infrastructure

**CLI Features**

- **Smart Output Resolution**: Automatic .txt file creation next to input files when no output specified
- **Directory Output Support**: Batch processing with organized output to specified directories  
- **File Conflict Handling**: Automatic numbering for directory outputs, overwrite protection for file outputs
- **Real-time Progress Feedback**: Emoji-enhanced status updates during transcription process
- **Multiple Input Format Detection**: Seamless handling of various audio/video formats

**Python API**

- **Simple Integration**: Clean API with `transcribe_audio_in_parallel()` function
- **Audio Utility Functions**: Duration calculation, segmentation by count/duration
- **Streaming Support**: BytesIO input support for in-memory audio processing
- **Performance Optimization**: Built-in parallel processing for large audio files

**Documentation and Usability**

- **Comprehensive README**: Detailed usage examples, CLI documentation, and cost comparison
- **Real-world Examples**: Practical use cases for researchers, content creators, and data analysts
- **Performance Benchmarking**: Speed and cost comparisons with commercial transcription services
