#!/usr/bin/env python3
"""
Video Analyzer CLI Entry Point
"""
import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from video_analyzer.main import skill_main
from video_analyzer.models import SummaryStyle


def main():
    parser = argparse.ArgumentParser(
        description="智能分析 Bilibili/YouTube/本地视频，生成转写、评估和总结"
    )
    parser.add_argument("--url", required=True, help="视频链接或本地文件路径")
    parser.add_argument(
        "--whisper-model",
        default="large-v2",
        help="Whisper 模型 (tiny/base/small/medium/large-v2/large-v3/turbo/distil-large-v2/distil-large-v3/distil-large-v3.5)",
    )
    parser.add_argument(
        "--analysis-types",
        default="evaluation,summary",
        help="分析类型，逗号分隔 (evaluation,summary,format)",
    )
    parser.add_argument(
        "--output-dir", default="./video-analysis", help="输出目录"
    )
    parser.add_argument(
        "--save-transcript",
        type=lambda x: x.lower() in ["true", "1", "yes"],
        default=True,
        help="是否保存原始转写",
    )
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument(
        "--summary-style",
        choices=["concise", "deep", "social", "study"],
        help="总结风格 (concise/deep/social/study)",
    )
    parser.add_argument(
        "--enable-screenshots",
        action="store_true",
        default=True,
        help="启用关键帧截图提取（默认启用，使用 --no-screenshots 禁用）",
    )
    parser.add_argument(
        "--no-screenshots",
        action="store_true",
        help="禁用关键帧截图提取",
    )

    args = parser.parse_args()

    # Parse analysis types
    analysis_types = [t.strip() for t in args.analysis_types.split(",")]

    # Map summary style
    style_map = {
        "concise": SummaryStyle.BRIEF_POINTS,
        "deep": SummaryStyle.DEEP_LONGFORM,
        "social": SummaryStyle.SOCIAL_MEDIA,
        "study": SummaryStyle.STUDY_NOTES,
    }
    summary_style = style_map.get(args.summary_style) if args.summary_style else None

    # Handle screenshot flag (default True, but can be disabled with --no-screenshots)
    enable_screenshots = args.enable_screenshots and not args.no_screenshots

    # Run analysis
    result = skill_main(
        url=args.url,
        whisper_model=args.whisper_model,
        analysis_types=analysis_types,
        output_dir=args.output_dir,
        save_transcript=args.save_transcript,
        config_path=args.config,
        summary_style=summary_style,
        enable_screenshots=enable_screenshots,
    )

    # Output result as JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
