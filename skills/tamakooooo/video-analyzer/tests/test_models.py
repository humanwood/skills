"""
Tests for models.py - SummaryStyle enum and helper functions.
"""

import pytest
from video_analyzer.models import (
    SummaryStyle,
    get_default_summary_style,
    calculate_screenshot_count,
    TranscriptSegment,
    KeyNode,
    ScreenshotResult,
)


class TestSummaryStyle:
    """Tests for SummaryStyle enum."""

    def test_summary_style_values(self):
        """Test that all expected styles exist."""
        assert SummaryStyle.BRIEF_POINTS.value == "brief_points"
        assert SummaryStyle.DEEP_LONGFORM.value == "deep_longform"
        assert SummaryStyle.SOCIAL_MEDIA.value == "social_media"
        assert SummaryStyle.STUDY_NOTES.value == "study_notes"

    def test_default_style(self):
        """Test that default style is DEEP_LONGFORM."""
        default = get_default_summary_style()
        assert default == SummaryStyle.DEEP_LONGFORM
        assert default.value == "deep_longform"

    def test_style_enum_members(self):
        """Test that all 4 styles are present."""
        styles = list(SummaryStyle)
        assert len(styles) == 4
        assert SummaryStyle.BRIEF_POINTS in styles
        assert SummaryStyle.DEEP_LONGFORM in styles
        assert SummaryStyle.SOCIAL_MEDIA in styles
        assert SummaryStyle.STUDY_NOTES in styles


class TestCalculateScreenshotCount:
    """Tests for calculate_screenshot_count function."""

    def test_duration_less_than_5_minutes(self):
        """Videos < 5 minutes should get 3 screenshots."""
        assert calculate_screenshot_count(60) == 3  # 1 minute
        assert calculate_screenshot_count(150) == 3  # 2.5 minutes
        assert calculate_screenshot_count(299) == 3  # 4.98 minutes

    def test_duration_5_to_20_minutes(self):
        """Videos 5-20 minutes should get 5 screenshots."""
        assert calculate_screenshot_count(300) == 5  # 5 minutes
        assert calculate_screenshot_count(600) == 5  # 10 minutes
        assert calculate_screenshot_count(1199) == 5  # 19.98 minutes

    def test_duration_20_to_60_minutes(self):
        """Videos 20-60 minutes should get 8 screenshots."""
        assert calculate_screenshot_count(1200) == 8  # 20 minutes
        assert calculate_screenshot_count(1800) == 8  # 30 minutes
        assert calculate_screenshot_count(3599) == 8  # 59.98 minutes

    def test_duration_over_60_minutes(self):
        """Videos > 60 minutes should get 12 screenshots."""
        assert calculate_screenshot_count(3600) == 12  # 60 minutes
        assert calculate_screenshot_count(7200) == 12  # 120 minutes
        assert calculate_screenshot_count(10800) == 12  # 180 minutes

    def test_boundary_conditions(self):
        """Test exact boundary values."""
        assert calculate_screenshot_count(300) == 5  # Exactly 5 minutes
        assert calculate_screenshot_count(1200) == 8  # Exactly 20 minutes
        assert calculate_screenshot_count(3600) == 12  # Exactly 60 minutes


class TestDataClasses:
    """Tests for dataclass models."""

    def test_transcript_segment(self):
        """Test TranscriptSegment dataclass."""
        segment = TranscriptSegment(start=0.0, end=5.5, text="Hello world")
        assert segment.start == 0.0
        assert segment.end == 5.5
        assert segment.text == "Hello world"

    def test_key_node(self):
        """Test KeyNode dataclass."""
        node = KeyNode(
            timestamp_seconds=125.5, title="Core Concept", importance_score=0.9
        )
        assert node.timestamp_seconds == 125.5
        assert node.title == "Core Concept"
        assert node.importance_score == 0.9

    def test_screenshot_result_success(self):
        """Test ScreenshotResult with success."""
        result = ScreenshotResult(
            file_paths=["/tmp/screenshot_1.jpg", "/tmp/screenshot_2.jpg"],
            timestamps=[10.0, 20.0],
            success=True,
            error_message=None,
        )
        assert result.success is True
        assert len(result.file_paths) == 2
        assert len(result.timestamps) == 2
        assert result.error_message is None

    def test_screenshot_result_failure(self):
        """Test ScreenshotResult with failure."""
        result = ScreenshotResult(
            file_paths=[], timestamps=[], success=False, error_message="ffmpeg failed"
        )
        assert result.success is False
        assert len(result.file_paths) == 0
        assert result.error_message == "ffmpeg failed"
