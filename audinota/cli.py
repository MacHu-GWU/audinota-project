# -*- coding: utf-8 -*-

"""
Command Line Interface for Audinota

This module provides the CLI for audio transcription using Python Fire.
"""

import io
from pathlib import Path
from typing import Optional

import fire

from audinota.api import transcribe_audio_in_parallel


def resolve_output_path(
    input_path: str,
    output_path: Optional[str],
    overwrite: bool,
) -> Path:
    """
    Resolve the final output file path based on input parameters.

    :param input_path: Path to the input audio file
    :param output_path: Optional output path (file or directory)
    :param overwrite: Whether to overwrite existing files

    :return: Resolved output file path

    :raises FileExistsError: If output file exists and overwrite is False
    """
    input_file = Path(input_path).absolute()

    if output_path is None:
        # Case 1: No output specified - create .txt next to input file
        base_name = input_file.stem
        output_dir = input_file.parent
        return _find_unique_filename(output_dir, base_name, ".txt")

    output_path_obj = Path(output_path)

    if output_path_obj.is_dir():
        # Case 2: Output is a directory - create .txt file in that directory
        base_name = input_file.stem
        return _find_unique_filename(output_path_obj, base_name, ".txt")

    # Case 3: Output is a file path
    if output_path_obj.exists() and not overwrite:
        raise FileExistsError(
            f"Output file '{output_path_obj}' already exists. "
            "Use --overwrite to overwrite the existing file."
        )

    return output_path_obj


def _find_unique_filename(
    directory: Path,
    base_name: str,
    extension: str,
) -> Path:
    """
    Find a unique filename by appending numbers if necessary.

    :param directory: Directory where the file will be created
    :param base_name: Base name of the file (without extension)
    :param extension: File extension (including the dot)

    :return: Path to a unique filename
    """
    # Try the base name first
    candidate = directory / f"{base_name}{extension}"
    if not candidate.exists():
        return candidate

    # Try numbered variations (01, 02, 03, ...)
    counter = 1
    while True:
        candidate = directory / f"{base_name}_{counter:02d}{extension}"
        if not candidate.exists():
            return candidate
        counter += 1

        # Safety check to avoid infinite loop
        if counter > 999:
            raise RuntimeError("Cannot find unique filename after 999 attempts")


class AudioTranscriber:
    """
    Audio transcription command-line interface.

    This class provides the main CLI functionality for transcribing audio files
    using the audinota library with intelligent parallel processing.
    """

    def transcribe(
        self,
        input: str,
        output: Optional[str] = None,
        overwrite: bool = False,
    ) -> None:
        """
        Transcribe an audio file to text using parallel processing.

        :param input: Path to the input audio file (required)
        :param output: Path to output file or directory (optional)
        :param overwrite: Whether to overwrite existing output files

        Example usage:
            audinota transcribe --input="podcast.mp3"
            audinota transcribe --input="lecture.mp4" --output="transcripts/"
            audinota transcribe --input="interview.wav" --output="result.txt" --overwrite
        """
        # Validate input file exists
        input_path = Path(input)
        if not input_path.exists():
            raise FileNotFoundError(f"Input audio file not found: {input}")

        if not input_path.is_file():
            raise ValueError(f"Input path is not a file: {input}")

        print(f"🎵 Transcribing audio file: {input_path}")

        # Resolve output path with all the logic
        try:
            output_path = resolve_output_path(input, output, overwrite)
            print(f"📝Output will be saved to: {output_path}")
        except FileExistsError as e:
            print(f"❌Error: {e}")
            return

        try:
            # Load audio file
            print("🔄Loading audio data...")
            audio_bytes = input_path.read_bytes()
            audio_stream = io.BytesIO(audio_bytes)

            # Perform transcription
            print("🚀Starting parallel transcription...")
            transcribed_text = transcribe_audio_in_parallel(audio_stream)

            # Save to output file
            print("💾Saving transcription...")
            try:
                output_path.write_text(transcribed_text, encoding="utf-8")
            except FileNotFoundError:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(transcribed_text, encoding="utf-8")

            print(f"✅Transcription completed successfully!")
            print(f"📄Output saved to: file://{output_path}")
            print(f"📊Text length: {len(transcribed_text)} characters")
        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            raise


def main():
    """
    Main entry point for the audinota CLI.

    This function is called when the 'audinota' command is run from the terminal.
    """
    fire.Fire(AudioTranscriber)
