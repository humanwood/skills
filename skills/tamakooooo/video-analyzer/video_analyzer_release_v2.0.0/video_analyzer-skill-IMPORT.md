# Video Analyzer Skill - 导入安装指南

## 📦 Skill 包信息

- **文件名**: `video_analyzer-skill-v2.0.0.tar.gz`
- **版本**: v2.0.0
- **大小**: 40KB
- **格式**: 标准 Claude Code Skill 包

## 🚀 快速导入

### 方法 1: 自动导入（推荐）

如果你使用的是支持 skill 导入的系统（如 Claude Code），可以直接导入：

```bash
# 解压到 skills 目录
cd ~/.claude/skills
tar -xzf /path/to/video_analyzer-skill-v2.0.0.tar.gz

# 系统会自动识别并加载 skill
```

### 方法 2: 手动安装

```bash
# 1. 创建 skills 目录（如果不存在）
mkdir -p ~/.claude/skills

# 2. 解压 skill 包
cd ~/.claude/skills
tar -xzf /path/to/video_analyzer-skill-v2.0.0.tar.gz

# 3. 进入 skill 目录
cd video_analyzer

# 4. 安装 Python 依赖
pip install -r requirements.txt

# 5. 安装 FFmpeg（系统依赖）
# Windows
winget install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg

# 6. 配置 API Key
cp config.example.json config.json
# 编辑 config.json，填入你的 API key
```

## 📋 Skill 包内容

解压后的目录结构：

```
video_analyzer/
├── SKILL.md                    # Skill 主文档（必需）
├── skill.yaml                  # Skill 配置文件
├── README.md                   # 使用文档
├── requirements.txt            # Python 依赖
├── config.example.json         # 配置示例
├── __init__.py                 # Python 包初始化
├── main.py                     # 主入口
├── run.py                      # 命令行启动脚本
├── core.py                     # 核心处理逻辑
├── transcriber.py              # 语音转写
├── llm_processor.py            # LLM 分析
├── downloader.py               # 视频下载
├── screenshot_extractor.py     # 截图提取
├── models.py                   # 数据模型
├── dependency_manager.py       # 依赖管理
├── bilibili_search.py          # B站搜索
├── prompts/                    # 提示词模板
│   ├── evaluation.md
│   ├── summary.md
│   ├── format.md
│   ├── key_node_selection.md
│   └── summary_styles/
│       ├── concise.md
│       ├── deep.md
│       ├── social.md
│       └── study.md
├── tests/                      # 测试文件
│   ├── conftest.py
│   ├── test_core_integration.py
│   ├── test_llm_processor_styles.py
│   ├── test_models.py
│   ├── test_screenshot_extractor.py
│   └── test_transcriber_timestamps.py
└── utils/                      # 工具函数
    ├── __init__.py
    ├── logger.py
    ├── progress.py
    └── temp_manager.py
```

## ⚙️ 配置说明

### 必需配置

编辑 `config.json`，配置 LLM API：

```json
{
  "llm": {
    "provider": "openai",
    "api_key": "your-api-key-here",
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

3. **其他兼容服务**
   ```json
   {
     "provider": "openai",
     "api_key": "your-key",
     "base_url": "https://your-endpoint.com/v1",
     "model": "gemini-3-flash"
   }
   ```

## 🧪 测试安装

安装完成后，运行测试命令：

```bash
cd ~/.claude/skills/video_analyzer

# 测试基础功能
python run.py --url "https://www.bilibili.com/video/BV1xx411c7mD" --whisper-model small

# 预期输出
# [1/5] Downloading video: ...
# [2/5] Transcribing with timestamps (model: small)...
# [3/5] Extracting screenshots...
# [4/5] Analyzing (2 types)...
# [5/5] Saving results...
# {
#   "success": true,
#   "video_title": "...",
#   ...
# }
```

## 📝 使用方法

### 在 Claude Code 中使用

当用户提到以下内容时，skill 会自动激活：
- "分析视频"
- "转写视频"
- "总结视频内容"
- "评估这个视频"
- "视频内容分析"

### 命令行使用

```bash
# 基础用法（自动启用截图）
python run.py --url "视频链接"

# 使用小模型加快速度
python run.py --url "视频链接" --whisper-model small

# 禁用截图功能
python run.py --url "视频链接" --no-screenshots

# 自定义总结风格
python run.py --url "视频链接" --summary-style deep
```

### Python API 使用

```python
from video_analyzer.main import skill_main

# 基础用法
result = skill_main("https://www.bilibili.com/video/BV1xx411c7mD")

# 高级配置
result = skill_main(
    url="https://www.youtube.com/watch?v=xxx",
    whisper_model="small",
    analysis_types=["evaluation", "summary"],
    output_dir="./my-analysis",
    enable_screenshots=True
)
```

## 🎯 功能特性

- ✅ 多平台支持（B站、YouTube、本地文件）
- ✅ 高精度语音转写（Whisper AI）
- ✅ 智能内容分析（评估、总结、格式化）
- ✅ 关键帧截图自动嵌入（默认启用）
- ✅ 智能节点选择（LLM 分析）
- ✅ 多种总结风格
- ✅ 批量处理支持

## ⚠️ 注意事项

1. **首次运行**：需要下载 Whisper 模型（自动下载）
   - small: 461MB（推荐测试）
   - large-v2: 2.87GB（推荐正式使用）

2. **系统要求**：
   - Python 3.8+
   - FFmpeg（必需）
   - 稳定的网络连接

3. **API 配置**：
   - 必须配置有效的 LLM API key
   - 支持 OpenAI、Anthropic 等多种提供商

4. **存储空间**：
   - 模型文件：~500MB - 3GB
   - 临时视频文件：根据视频大小
   - 分析结果：通常 < 1MB

## 🐛 故障排除

### 问题 1: 提示缺少 FFmpeg
**解决**：安装 FFmpeg
```bash
# Windows
winget install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

### 问题 2: API 调用失败
**解决**：检查 `config.json`
- API key 是否正确
- base_url 是否可访问
- 模型名称是否正确

### 问题 3: 模型下载失败
**解决**：
- 检查网络连接
- 使用 ModelScope 镜像（已配置）
- 手动下载模型文件

### 问题 4: 视频下载失败
**解决**：
- 检查视频 URL 是否有效
- 尝试使用本地视频文件
- 检查是否需要登录或代理

## 📚 相关文档

- `SKILL.md` - Skill 主文档
- `README.md` - 详细使用文档
- `skill.yaml` - Skill 配置
- `prompts/` - 提示词模板

## 🔄 更新日志

### v2.0.0 (2026-02-13)
- 默认启用关键帧截图功能
- 智能选择关键节点并自动嵌入截图
- 更新配置支持多种 LLM 模型
- 优化命令行参数处理
- 完善文档和示例

## 📞 技术支持

如有问题：
1. 查看日志：`logs/` 目录
2. 检查配置：`config.json`
3. 验证依赖：`pip list | grep whisper`
4. 阅读文档：`SKILL.md` 和 `README.md`

## 📄 许可证

与原项目保持一致

---

**打包时间**: 2026-02-13 00:39
**版本**: v2.0.0
**打包者**: Claude Code (Sonnet 4.5)
