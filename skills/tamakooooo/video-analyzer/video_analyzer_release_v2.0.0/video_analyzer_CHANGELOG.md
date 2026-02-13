# Video Analyzer v2.0.0 - 更新日志

## 📅 更新时间
2026-02-13 00:06

## 🎯 主要更新

### 1. 默认启用关键帧截图功能
- **变更**: `enable_screenshots` 默认值从 `false` 改为 `true`
- **影响**: 现在运行时会自动提取视频关键帧并插入到总结文档中
- **禁用方法**: 使用 `--no-screenshots` 参数

### 2. 智能关键节点选择
- 使用 LLM 分析转写内容，智能选择最重要的时间点
- 根据视频时长自动计算截图数量：
  - 0-5分钟：3张
  - 5-15分钟：5张
  - 15-30分钟：8张
  - 30-60分钟：12张
  - 60分钟以上：15张

### 3. 截图自动嵌入
- 截图会自动插入到总结文档的相应位置
- 每个关键节点都配有时间戳和标题说明

## 📝 文件修改

### 修改的文件
1. `run.py` - 更新命令行参数处理逻辑
2. `skill.yaml` - 更新默认配置和参数描述
3. `README.md` - 更新文档说明和示例代码

### 新增的文件
- 无（功能已在原代码中实现）

## 🔧 配置更新

### config.json
```json
{
  "llm": {
    "provider": "openai",
    "api_key": "ah-c389b32d7b202581bb5c01b6532086e3495a946926014b69f172e5916b28c768",
    "base_url": "https://api.tamako.online/v1",
    "model": "gemini-3-flash",
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

## 📦 备份信息

### 备份位置
1. **完整备份**: `C:\Users\10405\.claude\skills\video_analyzer_backup_20260213_000313\`
2. **干净压缩包**: `C:\Users\10405\Desktop\ai\video_analyzer_v2.0.0_clean_20260213_000605.tar.gz` (37KB)
3. **完整压缩包**: `C:\Users\10405\Desktop\ai\video_analyzer_v2.0.0_updated_20260213_000353.tar.gz` (3.1GB，包含模型)

### 备份说明
- 干净版本不包含：
  - `models/` 目录（Whisper 模型文件）
  - `video-analysis/` 目录（分析结果）
  - `__pycache__/` 目录（Python 缓存）
  - `config.json`（包含 API key）

## 🚀 使用方法

### 基础用法（自动启用截图）
```bash
python run.py --url "https://www.bilibili.com/video/BV1xx411c7mD"
```

### 禁用截图
```bash
python run.py --url "https://www.bilibili.com/video/BV1xx411c7mD" --no-screenshots
```

### 使用小模型加快速度
```bash
python run.py --url "https://www.bilibili.com/video/BV1xx411c7mD" --whisper-model small
```

## ⚠️ 注意事项

1. **首次运行**: 需要下载 Whisper 模型（small: 461MB, large-v2: 2.87GB）
2. **网络要求**: 启用截图需要下载完整视频（而非仅音频）
3. **处理时间**: 启用截图会增加处理时间（需要视频下载和截图提取）
4. **存储空间**: 截图会保存在 `output_dir/timestamp_screenshots/` 目录

## 🐛 已知问题

1. **网络不稳定**: 可能导致视频下载失败（SSL 错误）
2. **模型下载慢**: 首次运行需要等待模型下载完成

## 📊 测试结果

### 测试视频
- URL: https://www.bilibili.com/video/BV1AFc4zwEHA/
- 时长: 311.6秒（约5分钟）
- 转写字数: 5696字

### 测试结果
- ✅ 视频下载成功
- ✅ 语音转写成功
- ✅ LLM 分析成功（评估 + 总结）
- ✅ 生成 3 个 Markdown 文件

## 📚 相关文档

- README.md - 完整使用文档
- skill.yaml - 技能配置文件
- prompts/key_node_selection.md - 关键节点选择提示词

## 👤 更新者
Claude Code (Sonnet 4.5)

## 📄 许可证
与原项目保持一致
