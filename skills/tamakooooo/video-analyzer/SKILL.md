---
name: video-analyzer
version: 2.0.0
description: 智能分析 Bilibili/YouTube/本地视频，生成转写、评估和总结。支持关键帧截图自动嵌入。
author: user
tags: [video, transcription, analysis, bilibili, youtube, ai]
---

# Video Analyzer Skill

智能分析 Bilibili、YouTube 或本地视频，生成转写、评估和总结。支持关键帧截图自动嵌入。

## When to Use This Skill

当用户提到以下内容时激活此技能：
- "分析视频"
- "转写视频"
- "总结视频内容"
- "评估这个视频"
- "视频内容分析"
- "提取视频文字"
- "视频转文字"
- "B站视频分析"
- "YouTube 视频分析"

## How It Works

此技能会：
1. **下载视频**：支持 Bilibili、YouTube 或本地文件
2. **语音转写**：使用 Whisper AI 模型进行高精度转写
3. **关键帧提取**：智能选择关键节点并提取截图（默认启用）
4. **内容分析**：使用 LLM 进行内容评估、总结、格式化
5. **结果保存**：生成 Markdown 格式的分析报告

## Usage

### 基础用法

当用户请求分析视频时，调用 Python 脚本：

```bash
python .claude/skills/video_analyzer/run.py --url "<VIDEO_URL>"
```

### 参数说明

- `--url`: 视频链接或本地文件路径（必填）
- `--whisper-model`: Whisper 模型名称（默认: large-v2）
  - 可选: tiny, base, small, medium, large-v2, large-v3, turbo, distil-large-v2, distil-large-v3, distil-large-v3.5
- `--analysis-types`: 分析类型，多个用逗号分隔（默认: evaluation,summary）
  - 可选: evaluation, summary, format
- `--output-dir`: 输出目录（默认: ./video-analysis）
- `--save-transcript`: 是否保存原始转写（默认: true）
- `--summary-style`: 总结风格（可选: concise, deep, social, study）
- `--enable-screenshots`: 启用关键帧截图（默认: true）
- `--no-screenshots`: 禁用关键帧截图
- `--config`: 配置文件路径（可选）

### 使用示例

```bash
# 基础用法（自动启用截图）
python .claude/skills/video_analyzer/run.py --url "https://www.bilibili.com/video/BV1xx411c7mD"

# 使用小模型快速转写
python .claude/skills/video_analyzer/run.py --url "https://youtu.be/xxx" --whisper-model small

# 只做评估和总结
python .claude/skills/video_analyzer/run.py --url "./my-video.mp4" --analysis-types evaluation,summary

# 自定义输出目录
python .claude/skills/video_analyzer/run.py --url "https://www.bilibili.com/video/BV1xx411c7mD" --output-dir "./my-output"

# 禁用截图功能
python .claude/skills/video_analyzer/run.py --url "https://www.bilibili.com/video/BV1xx411c7mD" --no-screenshots

# 使用深度总结风格
python .claude/skills/video_analyzer/run.py --url "https://www.bilibili.com/video/BV1xx411c7mD" --summary-style deep
```

## Output

脚本会输出 JSON 格式的结果：

```json
{
  "success": true,
  "video_title": "视频标题",
  "duration_seconds": 311.6,
  "transcript_length": 5696,
  "output_files": {
    "transcript": "./video-analysis/xxx_transcript.md",
    "evaluation": "./video-analysis/xxx_evaluation.md",
    "summary": "./video-analysis/xxx_summary.md"
  },
  "summary": "Analyzed in 311.6s | 5696 chars | 2 analyses"
}
```

## Features

- 🎬 **多平台支持**: B站、YouTube、本地视频文件
- 🎤 **高精度转写**: 使用 Whisper AI 模型（支持多种模型大小）
- 🤖 **智能分析**: 内容评估、总结、格式化
- 📸 **关键帧截图**: 自动提取关键节点并配图（默认启用）
- 🎯 **智能节点选择**: 使用 LLM 分析选择最重要的时间点
- 📁 **文件输出**: Markdown 格式保存结果
- 🔍 **批量处理**: B站关键词搜索并批量分析
- 🌐 **多语言支持**: 支持中文、英文等多种语言

## Dependencies

首次运行会自动检查并安装依赖：

### Python 依赖
- Python 3.8+
- yt-dlp (>=2024.0.0) - 视频下载
- faster-whisper (>=1.0.0) - 语音转写
- modelscope (>=1.0.0) - 模型下载
- opencc-python-reimplemented - 繁简转换
- openai (>=1.0.0) - OpenAI API
- anthropic (>=0.18.0) - Anthropic API
- bilibili-api-python - B站 API
- tenacity (>=8.0.0) - 重试机制

### 系统依赖
- FFmpeg（必需）- 视频处理
- FFprobe（必需）- 视频信息提取

安装 FFmpeg：
```bash
# Windows
winget install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

## Configuration

如需使用 LLM 分析功能，需要配置 API key：

1. 复制 `config.example.json` 为 `config.json`
2. 填入你的 API key：

```json
{
  "llm": {
    "provider": "openai",
    "api_key": "your-api-key",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o-mini",
    "temperature": 0.3,
    "max_tokens": 12000
  },
  "transcribe": {
    "model_size": "large-v2",
    "cpu_threads": 4,
    "auto_optimize": true
  }
}
```

### 支持的 LLM 提供商

1. **OpenAI**
   ```json
   {
     "provider": "openai",
     "api_key": "sk-...",
     "base_url": "https://api.openai.com/v1",
     "model": "gpt-4o-mini"
   }
   ```

2. **Anthropic Claude**
   ```json
   {
     "provider": "anthropic",
     "api_key": "sk-ant-...",
     "model": "claude-3-5-sonnet-20241022"
   }
   ```

3. **兼容 OpenAI API 的服务**
   ```json
   {
     "provider": "openai",
     "api_key": "your-key",
     "base_url": "https://your-api-endpoint.com/v1",
     "model": "gemini-3-flash"
   }
   ```

## Analysis Types

| 类型 | 说明 |
|------|------|
| `evaluation` | 多维度内容评估（信息准确性、逻辑严谨性、价值稀缺性等） |
| `summary` | 高质量内容总结和重构 |
| `format` | 原始转写净化和格式化 |

## Summary Styles

| 风格 | 说明 |
|------|------|
| `concise` | 简洁要点式总结 |
| `deep` | 深度长文式总结（默认） |
| `social` | 社交媒体文案风格 |
| `study` | 学习笔记风格 |

## Screenshot Feature

启用截图功能后（默认启用），系统会：

1. **智能选择关键节点**：使用 LLM 分析转写内容，选择最重要的时间点
2. **自动计算数量**：根据视频时长自动确定截图数量
   - 0-5分钟：3张
   - 5-15分钟：5张
   - 15-30分钟：8张
   - 30-60分钟：12张
   - 60分钟以上：15张
3. **提取截图**：使用 FFmpeg 在关键时间点提取高质量截图
4. **嵌入文档**：自动将截图插入到总结文档的相应位置

## Notes

- 首次运行会下载 Whisper 模型（使用 ModelScope 国内镜像）
- 视频会临时下载到系统临时目录，分析完成后自动清理
- 支持繁简转换，输出统一为简体中文
- 大模型（large-v2/v3）转写精度更高但速度较慢
- 小模型（tiny/base）速度快但精度较低
- 启用截图需要下载完整视频（而非仅音频）

## Troubleshooting

### Q: 提示缺少 FFmpeg
**A**: 根据系统运行安装命令：
- Windows: `winget install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

### Q: 模型下载很慢
**A**: 使用 ModelScope 国内镜像，通常几分钟内完成

### Q: API 调用失败
**A**: 检查 `config.json` 中的 API key 是否正确

### Q: 视频下载失败
**A**: 可能原因：
- 网络不稳定（重试）
- 视频需要登录（使用本地文件）
- 地区限制（使用代理）

### Q: 截图功能不工作
**A**: 确保：
- FFmpeg 已正确安装
- 使用的是视频 URL（不是音频）
- 没有使用 `--no-screenshots` 参数

## Version History

### v2.0.0 (2026-02-13)
- 默认启用关键帧截图功能
- 智能选择关键节点并自动嵌入截图
- 更新配置文件支持 gemini-3-flash 模型
- 优化命令行参数处理
- 更新文档和示例代码

### v1.0.0
- 初始版本
- 支持视频转写和分析
- 支持多平台视频下载

## License

与原项目保持一致

## Author

user

## Support

如有问题，请检查：
1. 日志文件：`logs/` 目录
2. 配置文件：`config.json`
3. 依赖版本：`pip list | grep -E "whisper|openai|anthropic"`
