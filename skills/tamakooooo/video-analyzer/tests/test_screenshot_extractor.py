"""
Tests for screenshot_extractor.py - Screenshot extraction functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestScreenshotExtractor:
    """Tests for ScreenshotExtractor class."""

    def test_extract_returns_screenshot_result(self):
        """Test that extract() returns a ScreenshotResult object."""
        from video_analyzer.screenshot_extractor import ScreenshotExtractor
        from video_analyzer.models import ScreenshotResult

        with (
            patch("video_analyzer.screenshot_extractor.subprocess.run") as mock_run,
            patch("video_analyzer.screenshot_extractor.Path.exists", return_value=True),
        ):
            mock_run.return_value = Mock(returncode=0)
            extractor = ScreenshotExtractor()
            result = extractor.extract(
                video_path="/fake/video.mp4",
                timestamps=[10.0, 20.0],
                output_dir="/tmp/screenshots",
            )

            assert isinstance(result, ScreenshotResult)

    def test_extract_creates_output_directory(self):
        """Test that extract() creates the output directory if it doesn't exist."""
        from video_analyzer.screenshot_extractor import ScreenshotExtractor

        with (
            patch("video_analyzer.screenshot_extractor.subprocess.run") as mock_run,
            patch("video_analyzer.screenshot_extractor.Path") as mock_path,
        ):
            mock_run.return_value = Mock(returncode=0)
            mock_output_path = Mock()
            mock_output_path.exists.return_value = True
            mock_path.return_value = mock_output_path

            extractor = ScreenshotExtractor()
            extractor.extract(
                video_path="/fake/video.mp4",
                timestamps=[10.0],
                output_dir="/tmp/screenshots",
            )

            mock_output_path.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_extract_ffmpeg_command_format(self):
        """Test that ffmpeg is called with correct parameters."""
        from video_analyzer.screenshot_extractor import ScreenshotExtractor

        with (
            patch("video_analyzer.screenshot_extractor.subprocess.run") as mock_run,
            patch("video_analyzer.screenshot_extractor.Path.exists", return_value=True),
            patch("video_analyzer.screenshot_extractor.Path.mkdir"),
        ):
            mock_run.return_value = Mock(returncode=0)

            extractor = ScreenshotExtractor()
            extractor.extract(
                video_path="/fake/video.mp4", timestamps=[125.5], output_dir="/tmp"
            )

            # Verify ffmpeg was called
            mock_run.assert_called()
            call_args = mock_run.call_args[0][0]

            assert "ffmpeg" in call_args
            assert "-ss" in call_args
            assert "-i" in call_args
            assert "/fake/video.mp4" in call_args
            assert "-frames:v" in call_args
            assert "1" in call_args
            assert "-q:v" in call_args
            assert "2" in call_args

    def test_extract_deterministic_output_names(self):
        """Test that output filenames are deterministic (screenshot_{timestamp}s.jpg)."""
        from video_analyzer.screenshot_extractor import ScreenshotExtractor

        with (
            patch("video_analyzer.screenshot_extractor.subprocess.run") as mock_run,
            patch("video_analyzer.screenshot_extractor.Path") as mock_path,
        ):
            mock_run.return_value = Mock(returncode=0)
            mock_output_file = Mock()
            mock_output_file.exists.return_value = True
            mock_output_file.absolute.return_value = "/tmp/screenshot_125.5s.jpg"
            mock_path.return_value = mock_output_file

            extractor = ScreenshotExtractor()
            result = extractor.extract(
                video_path="/fake/video.mp4", timestamps=[125.5], output_dir="/tmp"
            )

            assert len(result.file_paths) > 0
            assert "screenshot_125.5s.jpg" in result.file_paths[0]

    def test_extract_non_fatal_individual_failures(self):
        """Test that individual screenshot failures don't abort entire operation."""
        from video_analyzer.screenshot_extractor import ScreenshotExtractor

        call_count = [0]

        def mock_run_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 2:  # Second call fails
                raise Exception("ffmpeg failed")
            return Mock(returncode=0)

        with (
            patch(
                "video_analyzer.screenshot_extractor.subprocess.run",
                side_effect=mock_run_side_effect,
            ),
            patch("video_analyzer.screenshot_extractor.Path") as mock_path,
        ):
            mock_output_file = Mock()
            mock_output_file.exists.return_value = True
            mock_output_file.absolute.return_value = "/tmp/screenshot.jpg"
            mock_path.return_value = mock_output_file

            extractor = ScreenshotExtractor()
            result = extractor.extract(
                video_path="/fake/video.mp4",
                timestamps=[10.0, 20.0, 30.0],
                output_dir="/tmp",
            )

            # Should get partial results (2 successes, 1 failure)
            assert result.success is True  # At least one succeeded
            assert len(result.file_paths) == 2  # Only successful extractions

    def test_extract_all_failures_returns_failure_result(self):
        """Test that if all screenshots fail, returns success=False."""
        from video_analyzer.screenshot_extractor import ScreenshotExtractor

        with (
            patch(
                "video_analyzer.screenshot_extractor.subprocess.run",
                side_effect=Exception("ffmpeg failed"),
            ),
            patch("video_analyzer.screenshot_extractor.Path.mkdir"),
        ):
            extractor = ScreenshotExtractor()
            result = extractor.extract(
                video_path="/fake/video.mp4", timestamps=[10.0, 20.0], output_dir="/tmp"
            )

            assert result.success is False
            assert len(result.file_paths) == 0
            assert result.error_message is not None

    def test_extract_video_not_found(self):
        """Test that extract handles missing video file gracefully."""
        from video_analyzer.screenshot_extractor import ScreenshotExtractor

        with patch("video_analyzer.screenshot_extractor.Path") as mock_path:
            mock_video_path = Mock()
            mock_video_path.exists.return_value = False

            extractor = ScreenshotExtractor()
            result = extractor.extract(
                video_path="/nonexistent/video.mp4",
                timestamps=[10.0],
                output_dir="/tmp",
            )

            assert result.success is False
            assert "not found" in result.error_message.lower()

    def test_extract_empty_timestamps_list(self):
        """Test that extract handles empty timestamps list."""
        from video_analyzer.screenshot_extractor import ScreenshotExtractor

        extractor = ScreenshotExtractor()
        result = extractor.extract(
            video_path="/fake/video.mp4", timestamps=[], output_dir="/tmp"
        )

        assert result.success is False
        assert "no timestamps" in result.error_message.lower()

    def test_extract_timeout_protection(self):
        """Test that subprocess has timeout protection (30s)."""
        from video_analyzer.screenshot_extractor import ScreenshotExtractor

        with (
            patch("video_analyzer.screenshot_extractor.subprocess.run") as mock_run,
            patch("video_analyzer.screenshot_extractor.Path.exists", return_value=True),
            patch("video_analyzer.screenshot_extractor.Path.mkdir"),
        ):
            mock_run.return_value = Mock(returncode=0)

            extractor = ScreenshotExtractor()
            extractor.extract(
                video_path="/fake/video.mp4", timestamps=[10.0], output_dir="/tmp"
            )

            # Verify timeout was set
            assert mock_run.call_args[1].get("timeout") == 30
