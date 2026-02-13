"""
Tests for core.py - Integration tests for screenshot workflow.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestCoreIntegration:
    """Integration tests for VideoAnalyzer core functionality."""

    def test_analyze_screenshots_disabled_uses_audio_path(
        self, mock_downloader, mock_transcriber, mock_llm_processor, temp_output_dir
    ):
        """Test that screenshots disabled follows audio-only path."""
        from video_analyzer.core import VideoAnalyzer

        with patch("video_analyzer.core.temp_manager") as mock_temp:
            analyzer = VideoAnalyzer(
                output_dir=str(temp_output_dir), enable_screenshots=False
            )
            analyzer._downloader = mock_downloader
            analyzer._transcriber = mock_transcriber
            analyzer._llm_processor = mock_llm_processor

            result = analyzer.analyze("https://example.com/video")

            # Should call get_audio, not get_video
            mock_downloader.get_audio.assert_called_once()
            mock_downloader.get_video.assert_not_called()

            # Should use regular transcribe, not timestamped
            mock_transcriber.transcribe.assert_called_once()
            mock_transcriber.transcribe_with_timestamps.assert_not_called()

    def test_analyze_screenshots_enabled_uses_video_path(
        self,
        mock_downloader,
        mock_transcriber,
        mock_llm_processor,
        mock_screenshot_extractor,
        temp_output_dir,
    ):
        """Test that screenshots enabled follows video path."""
        from video_analyzer.core import VideoAnalyzer

        with patch("video_analyzer.core.temp_manager") as mock_temp:
            analyzer = VideoAnalyzer(
                output_dir=str(temp_output_dir), enable_screenshots=True
            )
            analyzer._downloader = mock_downloader
            analyzer._transcriber = mock_transcriber
            analyzer._llm_processor = mock_llm_processor
            analyzer._screenshot_extractor = mock_screenshot_extractor

            result = analyzer.analyze("https://example.com/video")

            # Should call get_video, not get_audio
            mock_downloader.get_video.assert_called_once()
            mock_downloader.get_audio.assert_not_called()

            # Should use timestamped transcribe
            mock_transcriber.transcribe_with_timestamps.assert_called_once()

    def test_analyze_screenshots_calls_llm_key_nodes(
        self,
        mock_downloader,
        mock_transcriber,
        mock_llm_processor,
        mock_screenshot_extractor,
        temp_output_dir,
    ):
        """Test that screenshots enabled calls LLM for key node selection."""
        from video_analyzer.core import VideoAnalyzer

        with patch("video_analyzer.core.temp_manager") as mock_temp:
            analyzer = VideoAnalyzer(
                output_dir=str(temp_output_dir), enable_screenshots=True
            )
            analyzer._downloader = mock_downloader
            analyzer._transcriber = mock_transcriber
            analyzer._llm_processor = mock_llm_processor
            analyzer._screenshot_extractor = mock_screenshot_extractor

            result = analyzer.analyze("https://example.com/video")

            # Should call select_key_nodes
            mock_llm_processor.select_key_nodes.assert_called_once()

    def test_analyze_screenshots_calls_screenshot_extractor(
        self,
        mock_downloader,
        mock_transcriber,
        mock_llm_processor,
        mock_screenshot_extractor,
        temp_output_dir,
    ):
        """Test that screenshot extractor is called with correct parameters."""
        from video_analyzer.core import VideoAnalyzer

        with patch("video_analyzer.core.temp_manager") as mock_temp:
            analyzer = VideoAnalyzer(
                output_dir=str(temp_output_dir), enable_screenshots=True
            )
            analyzer._downloader = mock_downloader
            analyzer._transcriber = mock_transcriber
            analyzer._llm_processor = mock_llm_processor
            analyzer._screenshot_extractor = mock_screenshot_extractor

            result = analyzer.analyze("https://example.com/video")

            # Should call extract with timestamps from key nodes
            mock_screenshot_extractor.extract.assert_called_once()
            call_args = mock_screenshot_extractor.extract.call_args
            assert "timestamps" in call_args[1]

    def test_analyze_summary_style_calls_process_summary(
        self, mock_downloader, mock_transcriber, mock_llm_processor, temp_output_dir
    ):
        """Test that summary_style parameter calls process_summary."""
        from video_analyzer.core import VideoAnalyzer
        from video_analyzer.models import SummaryStyle

        with patch("video_analyzer.core.temp_manager") as mock_temp:
            analyzer = VideoAnalyzer(
                output_dir=str(temp_output_dir),
                summary_style=SummaryStyle.SOCIAL_MEDIA,
                analysis_types=["summary"],
            )
            analyzer._downloader = mock_downloader
            analyzer._transcriber = mock_transcriber
            analyzer._llm_processor = mock_llm_processor

            result = analyzer.analyze("https://example.com/video")

            # Should call process_summary with style
            mock_llm_processor.process_summary.assert_called_once()
            call_args = mock_llm_processor.process_summary.call_args
            assert call_args[1]["style"] == SummaryStyle.SOCIAL_MEDIA

    def test_analyze_no_summary_style_uses_default_process(
        self, mock_downloader, mock_transcriber, mock_llm_processor, temp_output_dir
    ):
        """Test that no summary_style uses default process method."""
        from video_analyzer.core import VideoAnalyzer

        with patch("video_analyzer.core.temp_manager") as mock_temp:
            analyzer = VideoAnalyzer(
                output_dir=str(temp_output_dir),
                summary_style=None,
                analysis_types=["summary"],
            )
            analyzer._downloader = mock_downloader
            analyzer._transcriber = mock_transcriber
            analyzer._llm_processor = mock_llm_processor

            result = analyzer.analyze("https://example.com/video")

            # Should call regular process, not process_summary
            mock_llm_processor.process.assert_called()

    def test_analyze_screenshots_non_fatal_failures(
        self,
        mock_downloader,
        mock_transcriber,
        mock_llm_processor,
        mock_screenshot_extractor,
        temp_output_dir,
    ):
        """Test that screenshot failures don't abort entire analysis."""
        from video_analyzer.core import VideoAnalyzer

        # Make screenshot extraction fail
        mock_screenshot_extractor.extract.side_effect = Exception("Screenshot failed")

        with patch("video_analyzer.core.temp_manager") as mock_temp:
            analyzer = VideoAnalyzer(
                output_dir=str(temp_output_dir),
                enable_screenshots=True,
                analysis_types=["summary"],
            )
            analyzer._downloader = mock_downloader
            analyzer._transcriber = mock_transcriber
            analyzer._llm_processor = mock_llm_processor
            analyzer._screenshot_extractor = mock_screenshot_extractor

            result = analyzer.analyze("https://example.com/video")

            # Analysis should still succeed
            assert result["success"] is True
            # Summary should still be processed
            mock_llm_processor.process.assert_called()

    def test_generate_summary_with_screenshots_inserts_images(self):
        """Test that _generate_summary_with_screenshots inserts inline images."""
        from video_analyzer.core import VideoAnalyzer

        analyzer = VideoAnalyzer()

        summary = """# Test Summary

## Introduction

Content here.

## Core Concepts

More content.
"""

        key_nodes = [
            {"title": "Introduction", "timestamp_seconds": 10.0},
            {"title": "Core Concepts", "timestamp_seconds": 20.0},
        ]

        screenshot_paths = ["/tmp/screenshot_10.0s.jpg", "/tmp/screenshot_20.0s.jpg"]

        result = analyzer._generate_summary_with_screenshots(
            summary_text=summary, key_nodes=key_nodes, screenshot_paths=screenshot_paths
        )

        # Should contain inline images
        assert "![Screenshot](/tmp/screenshot_10.0s.jpg)" in result
        assert "![Screenshot](/tmp/screenshot_20.0s.jpg)" in result

    def test_generate_summary_with_screenshots_matches_titles(self):
        """Test that screenshots are inserted after matching headers."""
        from video_analyzer.core import VideoAnalyzer

        analyzer = VideoAnalyzer()

        summary = """## Introduction to AI Agents

Content.

## Key Components

More content.
"""

        key_nodes = [{"title": "Introduction", "timestamp_seconds": 10.0}]

        screenshot_paths = ["/tmp/screenshot_10.0s.jpg"]

        result = analyzer._generate_summary_with_screenshots(
            summary_text=summary, key_nodes=key_nodes, screenshot_paths=screenshot_paths
        )

        # Should match "Introduction" with "Introduction to AI Agents"
        assert "![Screenshot]" in result

    def test_generate_summary_with_screenshots_empty_lists(self):
        """Test that empty key_nodes/screenshots returns original summary."""
        from video_analyzer.core import VideoAnalyzer

        analyzer = VideoAnalyzer()

        summary = "# Test Summary"

        result = analyzer._generate_summary_with_screenshots(
            summary_text=summary, key_nodes=[], screenshot_paths=[]
        )

        assert result == summary

    def test_backward_compatibility_default_parameters(
        self, mock_downloader, mock_transcriber, mock_llm_processor, temp_output_dir
    ):
        """Test that default parameters maintain backward compatibility."""
        from video_analyzer.core import VideoAnalyzer

        with patch("video_analyzer.core.temp_manager") as mock_temp:
            # Create analyzer with default params (no screenshots, no style)
            analyzer = VideoAnalyzer(output_dir=str(temp_output_dir))
            analyzer._downloader = mock_downloader
            analyzer._transcriber = mock_transcriber
            analyzer._llm_processor = mock_llm_processor

            # Should work exactly as before
            assert analyzer.enable_screenshots is False
            assert analyzer.summary_style is None

            result = analyzer.analyze("https://example.com/video")

            # Should use audio-only path
            mock_downloader.get_audio.assert_called_once()
            mock_transcriber.transcribe.assert_called_once()
