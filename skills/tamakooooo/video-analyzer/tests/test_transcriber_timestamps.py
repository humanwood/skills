"""
Tests for transcriber.py - transcribe_with_timestamps method.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestTranscriberTimestamps:
    """Tests for Transcriber.transcribe_with_timestamps method."""

    @patch("video_analyzer.transcriber.WhisperModel")
    def test_transcribe_with_timestamps_returns_list(self, mock_whisper_model):
        """Test that transcribe_with_timestamps returns a list of dicts."""
        from video_analyzer.transcriber import Transcriber

        # Mock WhisperModel
        mock_model = Mock()
        mock_segment1 = Mock()
        mock_segment1.start = 0.0
        mock_segment1.end = 5.5
        mock_segment1.text = " Hello world "

        mock_segment2 = Mock()
        mock_segment2.start = 5.5
        mock_segment2.end = 10.0
        mock_segment2.text = " Test segment "

        mock_model.transcribe.return_value = ([mock_segment1, mock_segment2], Mock())
        mock_whisper_model.return_value = mock_model

        transcriber = Transcriber(model_size="tiny")
        result = transcriber.transcribe_with_timestamps("/fake/audio.mp3")

        assert isinstance(result, list)
        assert len(result) == 2

    @patch("video_analyzer.transcriber.WhisperModel")
    def test_transcribe_with_timestamps_segment_structure(self, mock_whisper_model):
        """Test that each segment has start, end, text fields."""
        from video_analyzer.transcriber import Transcriber

        # Mock WhisperModel
        mock_model = Mock()
        mock_segment = Mock()
        mock_segment.start = 0.0
        mock_segment.end = 5.5
        mock_segment.text = " Hello world "

        mock_model.transcribe.return_value = ([mock_segment], Mock())
        mock_whisper_model.return_value = mock_model

        transcriber = Transcriber(model_size="tiny")
        result = transcriber.transcribe_with_timestamps("/fake/audio.mp3")

        assert len(result) == 1
        segment = result[0]
        assert "start" in segment
        assert "end" in segment
        assert "text" in segment
        assert isinstance(segment["start"], float)
        assert isinstance(segment["end"], float)
        assert isinstance(segment["text"], str)

    @patch("video_analyzer.transcriber.WhisperModel")
    def test_transcribe_with_timestamps_strips_whitespace(self, mock_whisper_model):
        """Test that text is stripped of leading/trailing whitespace."""
        from video_analyzer.transcriber import Transcriber

        # Mock WhisperModel
        mock_model = Mock()
        mock_segment = Mock()
        mock_segment.start = 0.0
        mock_segment.end = 5.5
        mock_segment.text = "  Whitespace test  "

        mock_model.transcribe.return_value = ([mock_segment], Mock())
        mock_whisper_model.return_value = mock_model

        transcriber = Transcriber(model_size="tiny")
        result = transcriber.transcribe_with_timestamps("/fake/audio.mp3")

        assert result[0]["text"] == "Whitespace test"

    @patch("video_analyzer.transcriber.WhisperModel")
    @patch("video_analyzer.transcriber.OpenCC")
    def test_transcribe_with_timestamps_traditional_to_simplified(
        self, mock_opencc, mock_whisper_model
    ):
        """Test that Traditional Chinese is converted to Simplified."""
        from video_analyzer.transcriber import Transcriber

        # Mock OpenCC conversion
        mock_converter = Mock()
        mock_converter.convert.return_value = "Simplified text"
        mock_opencc.return_value = mock_converter

        # Mock WhisperModel
        mock_model = Mock()
        mock_segment = Mock()
        mock_segment.start = 0.0
        mock_segment.end = 5.5
        mock_segment.text = "Traditional text"

        mock_model.transcribe.return_value = ([mock_segment], Mock())
        mock_whisper_model.return_value = mock_model

        transcriber = Transcriber(model_size="tiny")
        result = transcriber.transcribe_with_timestamps("/fake/audio.mp3")

        # Verify OpenCC was called
        mock_converter.convert.assert_called()
        assert result[0]["text"] == "Simplified text"

    @patch("video_analyzer.transcriber.WhisperModel")
    def test_transcribe_with_timestamps_preserves_order(self, mock_whisper_model):
        """Test that segments are returned in chronological order."""
        from video_analyzer.transcriber import Transcriber

        # Mock WhisperModel with multiple segments
        mock_model = Mock()
        segments = []
        for i in range(5):
            seg = Mock()
            seg.start = i * 5.0
            seg.end = (i + 1) * 5.0
            seg.text = f"Segment {i}"
            segments.append(seg)

        mock_model.transcribe.return_value = (segments, Mock())
        mock_whisper_model.return_value = mock_model

        transcriber = Transcriber(model_size="tiny")
        result = transcriber.transcribe_with_timestamps("/fake/audio.mp3")

        assert len(result) == 5
        for i, segment in enumerate(result):
            assert segment["start"] == i * 5.0
            assert segment["end"] == (i + 1) * 5.0
            assert segment["text"] == f"Segment {i}"

    @patch("video_analyzer.transcriber.WhisperModel")
    def test_original_transcribe_still_works(self, mock_whisper_model):
        """Test that original transcribe() method still works (backward compatibility)."""
        from video_analyzer.transcriber import Transcriber

        # Mock WhisperModel
        mock_model = Mock()
        mock_segment1 = Mock()
        mock_segment1.text = " Segment 1 "
        mock_segment2 = Mock()
        mock_segment2.text = " Segment 2 "

        mock_model.transcribe.return_value = ([mock_segment1, mock_segment2], Mock())
        mock_whisper_model.return_value = mock_model

        transcriber = Transcriber(model_size="tiny")
        result = transcriber.transcribe("/fake/audio.mp3")

        assert isinstance(result, str)
        assert "Segment 1" in result
        assert "Segment 2" in result
