╔══════════════════════════════════════════════════════════════════════╗
║              Video Analyzer Skill v2.0.0 - 发布包                    ║
╚══════════════════════════════════════════════════════════════════════╝

📦 包含文件
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. video_analyzer-skill-v2.0.0.tar.gz (40KB)
   ⭐ 主要 Skill 包，可直接导入使用

2. video_analyzer-QUICKSTART.txt (5KB)
   📖 快速开始指南，包含最常用的命令

3. video_analyzer-skill-IMPORT.md (7.5KB)
   📚 详细的导入和安装指南

4. video_analyzer-skill-PACKAGE.md (7.7KB)
   📋 完整的打包说明和功能介绍

5. video_analyzer_CHANGELOG.md (3.6KB)
   📝 版本更新日志

6. video_analyzer_VERSION.json (1.5KB)
   🔖 版本信息（JSON 格式）

7. README.txt (本文件)
   ℹ️ 发布包说明

🚀 快速开始
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. 解压 Skill 包
cd ~/.claude/skills
tar -xzf video_analyzer-skill-v2.0.0.tar.gz

# 2. 安装依赖
cd video_analyzer
pip install -r requirements.txt

# 3. 安装 FFmpeg
# Windows: winget install ffmpeg
# macOS:   brew install ffmpeg
# Linux:   sudo apt install ffmpeg

# 4. 配置 API
cp config.example.json config.json
# 编辑 config.json，填入你的 API key

# 5. 开始使用
python run.py --url "视频链接" --whisper-model small

🎯 主要功能
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 多平台支持（B站、YouTube、本地文件）
✅ 高精度语音转写（Whisper AI）
✅ 智能内容分析（评估、总结、格式化）
✅ 关键帧截图自动嵌入（默认启用）
✅ 智能节点选择（LLM 分析）
✅ 多种总结风格

⚠️ 系统要求
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Python 3.8+
✓ FFmpeg（必需）
✓ LLM API key（OpenAI/Anthropic/其他）

📚 详细文档
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
请查看以下文件获取更多信息：
- video_analyzer-QUICKSTART.txt - 快速参考
- video_analyzer-skill-IMPORT.md - 导入指南
- video_analyzer-skill-PACKAGE.md - 完整说明

🔒 数据脱敏说明
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
本发布包已进行数据脱敏处理：
✓ 已移除所有 API key 和敏感配置
✓ 已移除本地路径信息
✓ 已移除用户数据和缓存
✓ 仅包含通用配置示例

📄 许可证
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
与原项目保持一致

╔══════════════════════════════════════════════════════════════════════╗
║  版本: v2.0.0 | 发布日期: 2026-02-13 | 状态: ✅ 可以使用           ║
╚══════════════════════════════════════════════════════════════════════╝
