# Video Analyzer Skill v2.0.0

智能分析 Bilibili/YouTube/本地视频，生成转写、评估和总结。支持关键帧截图自动嵌入。

## 📦 包含文件

- `video_analyzer-skill-v2.0.0.tar.gz` - 主 Skill 包（40KB）
- `video_analyzer-skill-IMPORT.md` - 导入安装指南
- `video_analyzer-skill-PACKAGE.md` - 打包说明
- `video_analyzer-QUICKSTART.txt` - 快速参考卡片
- `video_analyzer_CHANGELOG.md` - 更新日志
- `video_analyzer_VERSION.json` - 版本信息
- `README.md` - 本文件

## 🚀 快速开始

### 1. 解压安装

```bash
cd ~/.claude/skills
tar -xzf video_analyzer-skill-v2.0.0.tar.gz
cd video_analyzer
pip install -r requirements.txt
```

### 2. 安装 FFmpeg

```bash
# Windows
winget install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

### 3. 配置 API

```bash
cp config.example.json config.json
# 编辑 config.json，填入你的 API key
```

### 4. 开始使用

```bash
python run.py --url "视频链接" --whisper-model small
```

## 🎯 功能特性

- ✅ 多平台支持（B站、YouTube、本地文件）
- ✅ 高精度语音转写（Whisper AI）
- ✅ 智能内容分析（评估、总结、格式化）
- ✅ 关键帧截图自动嵌入（默认启用）
- ✅ 智能节点选择（LLM 分析）
- ✅ 多种总结风格

## 📚 详细文档

请查看：
- `video_analyzer-skill-IMPORT.md` - 完整安装指南
- `video_analyzer-QUICKSTART.txt` - 快速参考
- `video_analyzer_CHANGELOG.md` - 更新日志

## ⚠️ 系统要求

- Python 3.8+
- FFmpeg（必需）
- LLM API key（OpenAI/Anthropic/其他）

## 📄 版本信息

- **版本**: v2.0.0
- **发布日期**: 2026-02-13
- **状态**: ✅ 可以使用

## 📞 技术支持

查看日志: logs/ 目录
检查配置: config.json
验证依赖: pip list | grep whisper
