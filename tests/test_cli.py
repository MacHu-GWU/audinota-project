# -*- coding: utf-8 -*-

from audinota.cli import (
    resolve_output_path,
)

import pytest
from audinota.paths import dir_unit_test

dir_tmp = dir_unit_test / "tmp"
dir_tmp.mkdir(parents=True, exist_ok=True)


def test_resolve_output_path():
    """
    Test the resolve_output_path function with various scenarios.
    """
    # Setup test files and directories
    p_input_audio = dir_tmp / "test_audio.mp3"
    p_input_audio.write_text("fake audio content", encoding="utf-8")

    output_dir = dir_tmp / "output_dir"
    output_dir.mkdir(exist_ok=True)

    # Test Case 1: input output both files, no conflict
    def test_case_1():
        """Test: input output both files, output has no conflict"""
        output_file = dir_tmp / "no_conflict.txt"
        # Ensure the file doesn't exist
        if output_file.exists():
            output_file.unlink()

        result = resolve_output_path(
            input_path=str(p_input_audio), output_path=str(output_file), overwrite=False
        )

        assert result == output_file
        assert result.is_absolute()

    # Test Case 2: input output both files, conflict exists, overwrite=False
    def test_case_2():
        """Test: input output both files, output has conflict, overwrite=False (should raise error)"""
        conflict_file = dir_tmp / "existing_conflict.txt"
        conflict_file.write_text("existing content", encoding="utf-8")

        with pytest.raises(FileExistsError) as exc_info:
            resolve_output_path(
                input_path=str(p_input_audio),
                output_path=str(conflict_file),
                overwrite=False,
            )

        assert "already exists" in str(exc_info.value)
        assert "Use --overwrite" in str(exc_info.value)

    # Test Case 3: input output both files, conflict exists, overwrite=True
    def test_case_3():
        """Test: input output both files, output has conflict, overwrite=True (should succeed)"""
        conflict_file = dir_tmp / "overwrite_conflict.txt"
        conflict_file.write_text("existing content", encoding="utf-8")

        result = resolve_output_path(
            input_path=str(p_input_audio),
            output_path=str(conflict_file),
            overwrite=True,
        )

        assert result == conflict_file
        assert result.exists()  # File should still exist

    # Test Case 4: output is directory, no filename conflict
    def test_case_4():
        """Test: output is directory, no filename conflict"""
        # Ensure target file doesn't exist
        target_file = output_dir / "test_audio.txt"
        if target_file.exists():
            target_file.unlink()

        result = resolve_output_path(
            input_path=str(p_input_audio), output_path=str(output_dir), overwrite=False
        )

        expected = output_dir / "test_audio.txt"
        assert result == expected
        assert result.name == "test_audio.txt"

    # Test Case 5: output is directory, filename conflict (should auto-number)
    def test_case_5():
        """Test: output is directory, filename conflict (should add _01, _02 suffixes)"""
        # Create conflicting files
        base_file = output_dir / "conflict_audio.txt"
        conflict_file_01 = output_dir / "conflict_audio_01.txt"
        conflict_file_02 = output_dir / "conflict_audio_02.txt"

        base_file.write_text("content 0", encoding="utf-8")
        conflict_file_01.write_text("content 1", encoding="utf-8")
        conflict_file_02.write_text("content 2", encoding="utf-8")

        # Create input file with matching stem
        conflict_input = dir_tmp / "conflict_audio.mp3"
        conflict_input.write_text("fake audio", encoding="utf-8")

        result = resolve_output_path(
            input_path=str(conflict_input),
            output_path=str(output_dir),
            overwrite=False,  # overwrite doesn't matter for directory case
        )

        expected = output_dir / "conflict_audio_03.txt"
        assert result == expected
        assert result.name == "conflict_audio_03.txt"
        assert not result.exists()  # Should return non-existing file

    # Test Case 6: No output path specified (should create next to input)
    def test_case_6():
        """Test: No output path specified - should create .txt next to input file"""
        result = resolve_output_path(
            input_path=str(p_input_audio), output_path=None, overwrite=False
        )

        expected = p_input_audio.parent / "test_audio.txt"
        assert result == expected
        assert result.name == "test_audio.txt"

    # Test Case 7: No output path, input filename conflicts
    def test_case_7():
        """Test: No output path, but input.txt already exists (should auto-number)"""
        # Create conflicting file next to input
        conflict_input = dir_tmp / "auto_number_test.mp3"
        conflict_input.write_text("fake audio", encoding="utf-8")

        existing_txt = dir_tmp / "auto_number_test.txt"
        existing_txt.write_text("existing", encoding="utf-8")

        result = resolve_output_path(
            input_path=str(conflict_input), output_path=None, overwrite=False
        )

        expected = dir_tmp / "auto_number_test_01.txt"
        assert result == expected
        assert result.name == "auto_number_test_01.txt"

    # Run all test cases
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    test_case_6()
    test_case_7()

    print("✅ All test cases passed!")
    print("📋 Test Summary:")
    print("   ✅ Case 1: No file conflict - ✓")
    print("   ✅ Case 2: File conflict, overwrite=False (FileExistsError) - ✓")
    print("   ✅ Case 3: File conflict, overwrite=True - ✓")
    print("   ✅ Case 4: Directory output, no conflict - ✓")
    print("   ✅ Case 5: Directory output, auto-numbering (_03) - ✓")
    print("   ✅ Case 6: No output path (default behavior) - ✓")
    print("   ✅ Case 7: No output path, auto-numbering (_01) - ✓")


if __name__ == "__main__":
    from audinota.tests import run_cov_test

    run_cov_test(
        __file__,
        "audinota.cli",
        preview=False,
    )
