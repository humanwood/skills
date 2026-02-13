"""
Pytest configuration and shared fixtures for video analyzer tests.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock
from typing import List, Dict, Any


@pytest.fixture
def mock_llm_response():
    """Mock LLM response text."""
    return "This is a test summary response."


@pytest.fixture
def mock_timestamped_transcript():
    """Mock timestamped transcript data."""
    return [
        {"start": 0.0, "end": 5.5, "text": "Hello and welcome to this video."},
        {"start": 5.5, "end": 12.0, "text": "Today we will discuss AI agents."},
        {"start": 12.0, "end": 20.5, "text": "First, let's understand the concept."},
        {"start": 20.5, "end": 30.0, "text": "An agent has three key components."},
    ]


@pytest.fixture
def mock_key_nodes():
    """Mock key nodes for screenshot extraction."""
    return [
        {
            "timestamp_seconds": 5.5,
            "title": "Introduction to AI Agents",
            "importance_score": 0.9,
        },
        {
            "timestamp_seconds": 12.0,
            "title": "Core Concepts",
            "importance_score": 0.85,
        },
        {
            "timestamp_seconds": 20.5,
            "title": "Key Components",
            "importance_score": 0.8,
        },
    ]


@pytest.fixture
def mock_video_info():
    """Mock video info dictionary."""
    return {
        "title": "Test Video",
        "url": "https://example.com/video",
        "platform": "YouTube",
        "duration": 600,  # 10 minutes
    }


@pytest.fixture
def mock_transcriber():
    """Mock Transcriber with transcribe_with_timestamps method."""
    transcriber = Mock()
    transcriber.transcribe_with_timestamps.return_value = [
        {"start": 0.0, "end": 5.5, "text": "Test segment 1"},
        {"start": 5.5, "end": 10.0, "text": "Test segment 2"},
    ]
    transcriber.transcribe.return_value = "Test segment 1 Test segment 2"
    return transcriber


@pytest.fixture
def mock_downloader():
    """Mock Downloader with get_video and get_audio methods."""
    downloader = Mock()
    downloader.get_video.return_value = (
        "/tmp/test_video.mp4",
        {
            "title": "Test Video",
            "url": "https://example.com/video",
            "platform": "YouTube",
            "duration": 600,
        },
    )
    downloader.get_audio.return_value = (
        "/tmp/test_audio.mp3",
        {
            "title": "Test Video",
            "url": "https://example.com/video",
            "platform": "YouTube",
        },
    )
    return downloader


@pytest.fixture
def mock_llm_processor():
    """Mock LLMProcessor with new methods."""
    processor = Mock()
    processor.process.return_value = "Standard summary response"
    processor.process_summary.return_value = "Styled summary response"
    processor.select_key_nodes.return_value = [
        {"timestamp_seconds": 5.5, "title": "Key Point 1", "importance_score": 0.9},
        {"timestamp_seconds": 12.0, "title": "Key Point 2", "importance_score": 0.85},
    ]
    return processor


@pytest.fixture
def mock_screenshot_extractor():
    """Mock ScreenshotExtractor."""
    from unittest.mock import MagicMock

    extractor = Mock()
    result = MagicMock()
    result.success = True
    result.file_paths = ["/tmp/screenshot_5.5s.jpg", "/tmp/screenshot_12.0s.jpg"]
    result.timestamps = [5.5, 12.0]
    result.error_message = None
    extractor.extract.return_value = result
    return extractor


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory for tests."""
    output_dir = tmp_path / "video-analysis"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def mock_summary_text():
    """Mock summary text with headers for screenshot insertion."""
    return """# Video Analysis Summary

## Introduction to AI Agents

This section covers the basics of AI agents.

## Core Concepts

Here we discuss the fundamental concepts.

## Key Components

The three key components are explained here.

## Conclusion

Summary of the main points.
"""
