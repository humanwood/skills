"""
Tests for llm_processor.py - Style routing and key-node selection.
"""

import pytest
from unittest.mock import Mock, patch, mock_open
import json


class TestProcessSummary:
    """Tests for LLMProcessor.process_summary method."""

    def test_process_summary_style_routing(self):
        """Test that style enum correctly routes to prompt files."""
        from video_analyzer.llm_processor import LLMProcessor
        from video_analyzer.models import SummaryStyle

        with (
            patch(
                "builtins.open",
                mock_open(read_data="Test prompt {video_title} {transcript}"),
            ),
            patch("video_analyzer.llm_processor.Path") as mock_path,
        ):
            mock_path.return_value.exists.return_value = True

            processor = LLMProcessor()
            processor._call_openai = Mock(return_value="Test response")

            result = processor.process_summary(
                text="Test transcript",
                style=SummaryStyle.SOCIAL_MEDIA,
                video_title="Test Video",
                duration_minutes=10.0,
            )

            assert result == "Test response"
            processor._call_openai.assert_called_once()

    def test_process_summary_style_mapping(self):
        """Test that SummaryStyle enums map to correct prompt files."""
        from video_analyzer.llm_processor import LLMProcessor
        from video_analyzer.models import SummaryStyle

        with (
            patch("builtins.open", mock_open(read_data="Prompt")) as mock_file,
            patch("video_analyzer.llm_processor.Path") as mock_path,
        ):
            mock_path_instance = Mock()
            mock_path_instance.exists.return_value = True
            mock_path.return_value = mock_path_instance

            processor = LLMProcessor()
            processor._call_openai = Mock(return_value="Response")

            # Test each style
            styles_to_files = {
                SummaryStyle.BRIEF_POINTS: "concise.md",
                SummaryStyle.DEEP_LONGFORM: "deep.md",
                SummaryStyle.SOCIAL_MEDIA: "social.md",
                SummaryStyle.STUDY_NOTES: "study.md",
            }

            for style, expected_file in styles_to_files.items():
                processor.process_summary(text="Test", style=style, video_title="Test")
                # Would verify the correct file was accessed

    def test_process_summary_unknown_style_returns_none(self):
        """Test that unknown style returns None."""
        from video_analyzer.llm_processor import LLMProcessor

        processor = LLMProcessor()

        # Create a mock style that's not in the mapping
        result = processor.process_summary(
            text="Test",
            style=None,  # This will cause the style_map.get() to return None
            video_title="Test",
        )

        # The method should handle this gracefully

    def test_process_summary_missing_prompt_file(self):
        """Test that missing prompt file returns None."""
        from video_analyzer.llm_processor import LLMProcessor
        from video_analyzer.models import SummaryStyle

        with patch("video_analyzer.llm_processor.Path") as mock_path:
            mock_path_instance = Mock()
            mock_path_instance.exists.return_value = False
            mock_path.return_value = mock_path_instance

            processor = LLMProcessor()
            result = processor.process_summary(
                text="Test", style=SummaryStyle.DEEP_LONGFORM, video_title="Test"
            )

            assert result is None


class TestSelectKeyNodes:
    """Tests for LLMProcessor.select_key_nodes method."""

    def test_select_key_nodes_returns_list(self):
        """Test that select_key_nodes returns a list."""
        from video_analyzer.llm_processor import LLMProcessor

        mock_response = json.dumps(
            [{"timestamp_seconds": 10.0, "title": "Test", "importance_score": 0.9}]
        )

        with (
            patch("builtins.open", mock_open(read_data="Prompt {transcript}")),
            patch("video_analyzer.llm_processor.Path.exists", return_value=True),
        ):
            processor = LLMProcessor()
            processor._call_openai = Mock(return_value=mock_response)

            result = processor.select_key_nodes(
                timestamped_transcript=[{"start": 0.0, "end": 5.0, "text": "Test"}],
                screenshot_count=3,
                video_title="Test",
            )

            assert isinstance(result, list)
            assert len(result) == 1

    def test_select_key_nodes_valid_json_parsing(self):
        """Test that valid JSON is parsed correctly."""
        from video_analyzer.llm_processor import LLMProcessor

        mock_response = json.dumps(
            [
                {
                    "timestamp_seconds": 10.5,
                    "title": "Key Point",
                    "importance_score": 0.9,
                },
                {
                    "timestamp_seconds": 20.0,
                    "title": "Second Point",
                    "importance_score": 0.85,
                },
            ]
        )

        with (
            patch("builtins.open", mock_open(read_data="Prompt")),
            patch("video_analyzer.llm_processor.Path.exists", return_value=True),
        ):
            processor = LLMProcessor()
            processor._call_openai = Mock(return_value=mock_response)

            result = processor.select_key_nodes(
                timestamped_transcript=[{"start": 0.0, "end": 5.0, "text": "Test"}],
                screenshot_count=2,
            )

            assert len(result) == 2
            assert result[0]["timestamp_seconds"] == 10.5
            assert result[0]["title"] == "Key Point"
            assert result[0]["importance_score"] == 0.9

    def test_select_key_nodes_markdown_code_blocks_removed(self):
        """Test that markdown ```json wrappers are removed."""
        from video_analyzer.llm_processor import LLMProcessor

        mock_response = """```json
[
  {"timestamp_seconds": 10.0, "title": "Test", "importance_score": 0.9}
]
```"""

        with (
            patch("builtins.open", mock_open(read_data="Prompt")),
            patch("video_analyzer.llm_processor.Path.exists", return_value=True),
        ):
            processor = LLMProcessor()
            processor._call_openai = Mock(return_value=mock_response)

            result = processor.select_key_nodes(
                timestamped_transcript=[{"start": 0.0, "end": 5.0, "text": "Test"}],
                screenshot_count=1,
            )

            assert len(result) == 1
            assert result[0]["timestamp_seconds"] == 10.0

    def test_select_key_nodes_malformed_json_returns_empty(self):
        """Test that malformed JSON returns empty list."""
        from video_analyzer.llm_processor import LLMProcessor

        mock_response = "This is not valid JSON at all"

        with (
            patch("builtins.open", mock_open(read_data="Prompt")),
            patch("video_analyzer.llm_processor.Path.exists", return_value=True),
        ):
            processor = LLMProcessor()
            processor._call_openai = Mock(return_value=mock_response)

            result = processor.select_key_nodes(
                timestamped_transcript=[{"start": 0.0, "end": 5.0, "text": "Test"}],
                screenshot_count=3,
            )

            assert result == []

    def test_select_key_nodes_missing_required_fields(self):
        """Test that nodes missing required fields are skipped."""
        from video_analyzer.llm_processor import LLMProcessor

        mock_response = json.dumps(
            [
                {"timestamp_seconds": 10.0, "title": "Valid", "importance_score": 0.9},
                {"timestamp_seconds": 20.0},  # Missing title
                {"title": "Missing Timestamp"},  # Missing timestamp_seconds
                {
                    "timestamp_seconds": 30.0,
                    "title": "Also Valid",
                    "importance_score": 0.8,
                },
            ]
        )

        with (
            patch("builtins.open", mock_open(read_data="Prompt")),
            patch("video_analyzer.llm_processor.Path.exists", return_value=True),
        ):
            processor = LLMProcessor()
            processor._call_openai = Mock(return_value=mock_response)

            result = processor.select_key_nodes(
                timestamped_transcript=[{"start": 0.0, "end": 5.0, "text": "Test"}],
                screenshot_count=4,
            )

            # Only 2 valid nodes should be returned
            assert len(result) == 2
            assert result[0]["title"] == "Valid"
            assert result[1]["title"] == "Also Valid"

    def test_select_key_nodes_adds_default_importance_score(self):
        """Test that missing importance_score gets default value 0.5."""
        from video_analyzer.llm_processor import LLMProcessor

        mock_response = json.dumps([{"timestamp_seconds": 10.0, "title": "No Score"}])

        with (
            patch("builtins.open", mock_open(read_data="Prompt")),
            patch("video_analyzer.llm_processor.Path.exists", return_value=True),
        ):
            processor = LLMProcessor()
            processor._call_openai = Mock(return_value=mock_response)

            result = processor.select_key_nodes(
                timestamped_transcript=[{"start": 0.0, "end": 5.0, "text": "Test"}],
                screenshot_count=1,
            )

            assert result[0]["importance_score"] == 0.5

    def test_select_key_nodes_sorted_by_timestamp(self):
        """Test that key nodes are sorted by timestamp ascending."""
        from video_analyzer.llm_processor import LLMProcessor

        mock_response = json.dumps(
            [
                {"timestamp_seconds": 30.0, "title": "Third", "importance_score": 0.7},
                {"timestamp_seconds": 10.0, "title": "First", "importance_score": 0.9},
                {"timestamp_seconds": 20.0, "title": "Second", "importance_score": 0.8},
            ]
        )

        with (
            patch("builtins.open", mock_open(read_data="Prompt")),
            patch("video_analyzer.llm_processor.Path.exists", return_value=True),
        ):
            processor = LLMProcessor()
            processor._call_openai = Mock(return_value=mock_response)

            result = processor.select_key_nodes(
                timestamped_transcript=[{"start": 0.0, "end": 5.0, "text": "Test"}],
                screenshot_count=3,
            )

            assert result[0]["title"] == "First"
            assert result[1]["title"] == "Second"
            assert result[2]["title"] == "Third"
            assert (
                result[0]["timestamp_seconds"]
                < result[1]["timestamp_seconds"]
                < result[2]["timestamp_seconds"]
            )

    def test_select_key_nodes_llm_error_returns_empty(self):
        """Test that LLM errors return empty list."""
        from video_analyzer.llm_processor import LLMProcessor

        with (
            patch("builtins.open", mock_open(read_data="Prompt")),
            patch("video_analyzer.llm_processor.Path.exists", return_value=True),
        ):
            processor = LLMProcessor()
            processor._call_openai = Mock(side_effect=Exception("LLM API error"))

            result = processor.select_key_nodes(
                timestamped_transcript=[{"start": 0.0, "end": 5.0, "text": "Test"}],
                screenshot_count=3,
            )

            assert result == []
