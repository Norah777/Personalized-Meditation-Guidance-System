# Peace Processor Pipeline 服务使用说明

本项目已被改造为服务形式，可以通过REST API调用pipeline功能。

## 🚀 新功能：分步骤生成

现在支持分步骤生成冥想内容：
1. **生成文本** → 2. **生成图片** → 3. **生成视频**

每个步骤都可以独立调用，提供更灵活的使用方式。

## 📂 文件说明

- `service.py` - Flask服务主文件，包含所有API端点
- `call_service.py` - 完整的客户端调用脚本
- `call_pipeline_service.py` - 简化的客户端调用脚本（推荐）
- `main.py` - 原始命令行版本（已保留，但推荐使用服务版本）

## 🛠️ API 端点

### 1. 生成文本 `/generate-text`
生成个性化冥想文本内容。

```bash
curl -X POST http://localhost:8008/generate-text \
  -H "Content-Type: application/json" \
  -d '{
    "user_prompt": "我想要一个关于森林中冥想的指导",
    "emotional_state": "放鬆"
  }'
```

**响应示例：**
```json
{
  "success": true,
  "text": "Begin by finding a comfortable position...",
  "message": "Text generation completed successfully"
}
```

### 2. 生成图片 `/generate-image`
基于文本内容生成冥想图片。

```bash
curl -X POST http://localhost:8008/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "text_content": "Begin by finding a comfortable position...",
    "output_path": "my_output"
  }'
```

**响应示例：**
```json
{
  "success": true,
  "image_path": "my_output/20240109_143022/image.png",
  "message": "Image generation completed successfully"
}
```

### 3. 生成视频 `/generate-video`
基于文本内容和图片生成冥想视频。

```bash
curl -X POST http://localhost:8008/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "text_content": "Begin by finding a comfortable position...",
    "image_path": "my_output/20240109_143022/image.png",
    "output_path": "my_output"
  }'
```

**响应示例：**
```json
{
  "success": true,
  "video_path": "my_output/20240109_143022/final_video.mp4",
  "message": "Video generation completed successfully"
}
```

### 4. 流式文本生成 `/generate-text-stream`
实时流式生成文本内容（Server-Sent Events）。

```bash
curl -X POST http://localhost:8008/generate-text-stream \
  -H "Content-Type: application/json" \
  -d '{
    "user_prompt": "我想要一个关于森林中冥想的指导",
    "emotional_state": "放鬆"
  }'
```

### 5. 完整管道 `/process` (原有功能)
一次性生成完整的冥想视频。

```bash
curl -X POST http://localhost:8008/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_prompt": "我想要一个关于森林中冥想的指导",
    "emotional_state": "放鬆",
    "output_path": "my_output"
  }'
```

## 🔧 使用方式

### 方式一：分步骤生成（推荐）

**步骤1：生成文本**
```bash
# 1. 生成文本
curl -X POST http://localhost:8008/generate-text \
  -H "Content-Type: application/json" \
  -d '{"user_prompt": "我感到焦虑，需要冥想指导", "emotional_state": "焦虑"}'
```

**步骤2：生成图片**
```bash
# 2. 使用生成的文本创建图片
curl -X POST http://localhost:8008/generate-image \
  -H "Content-Type: application/json" \
  -d '{"text_content": "生成的冥想文本内容..."}'
```

**步骤3：生成视频**
```bash
# 3. 使用文本和图片创建视频
curl -X POST http://localhost:8008/generate-video \
  -H "Content-Type: application/json" \
  -d '{"text_content": "生成的冥想文本内容...", "image_path": "output/xxx/image.png"}'
```

### 方式二：使用客户端脚本

**简化脚本（推荐）**：
```bash
python call_pipeline_service.py --user_prompt "帮助我放松"
```

**完整脚本**：
```bash
python call_service.py --user_prompt "帮助我放松"
```

### 方式三：完整管道一次性生成

```bash
curl -X POST http://localhost:8008/process \
  -H "Content-Type: application/json" \
  -d '{"user_prompt": "帮助我放松"}'
```

## 📋 参数说明

### 文本生成参数
- `user_prompt` (必需): 用户输入的提示词
- `emotional_state` (可选): 用户情绪状态，默认为 "neutral"

### 图片生成参数
- `text_content` (必需): 用于生成图片的文本内容
- `output_path` (可选): 输出路径，默认为 "output"

### 视频生成参数
- `text_content` (必需): 用于生成视频的文本内容
- `image_path` (可选): 图片文件路径，如果不提供会自动生成
- `output_path` (可选): 输出路径，默认为 "output"

### 完整管道参数
- `user_prompt` (必需): 用户输入的提示词
- `emotional_state` (可选): 用户情绪状态，默认为 "neutral"
- `output_path` (可选): 输出路径，默认为 "output"

## 📁 输出说明

### 文件结构
```
output/
└── 20240109_143022/          # 时间戳文件夹
    ├── script.txt            # 生成的文本脚本
    ├── image.png             # 生成的图片
    ├── narration.mp3         # 语音文件
    └── final_video.mp4       # 最终视频
```

### 返回路径格式
- **文本生成**: 直接返回文本内容
- **图片生成**: `{output_path}/{timestamp}/image.png`
- **视频生成**: `{output_path}/{timestamp}/final_video.mp4`

## ⚡ 性能优化

### 分步骤生成的优势
1. **快速响应**: 文本生成速度最快，用户可以立即看到结果
2. **按需生成**: 可以选择性地生成图片或视频
3. **资源节约**: 避免不必要的计算资源消耗
4. **更好的用户体验**: 提供实时反馈

### 推荐工作流程
1. 先调用 `/generate-text` 生成文本
2. 用户确认文本内容满意后，再选择生成图片或视频
3. 可以重复使用同一文本生成多个图片或视频

## 🔍 健康检查

检查服务状态：
```bash
curl http://localhost:8008/health
```

## 📖 快速开始示例

### 完整的分步骤生成示例

```bash
# 1. 启动服务
python service.py

# 2. 生成文本
curl -X POST http://localhost:8008/generate-text \
  -H "Content-Type: application/json" \
  -d '{"user_prompt": "我需要放松", "emotional_state": "紧张"}'

# 3. 生成图片
curl -X POST http://localhost:8008/generate-image \
  -H "Content-Type: application/json" \
  -d '{"text_content": "Begin by finding a comfortable position..."}'

# 4. 生成视频
curl -X POST http://localhost:8008/generate-video \
  -H "Content-Type: application/json" \
  -d '{"text_content": "Begin by finding a comfortable position...", "image_path": "output/20240109_143022/image.png"}'
```

## 📝 注意事项

1. 确保服务在调用客户端脚本之前已经启动
2. 第一次运行可能需要下载模型，耗时较长
3. 服务默认运行在端口8008，确保该端口未被占用
4. 生成的文件保存在时间戳文件夹内，便于管理
5. 分步骤生成时，建议保存中间结果的路径，以便后续使用
6. 流式文本生成适合需要实时反馈的场景

## 🔧 错误处理

### 常见错误响应
```json
{
  "success": false,
  "message": "错误信息描述"
}
```

### 错误码说明
- `400`: 请求参数错误
- `500`: 服务内部错误

## 🎯 使用建议

1. **开发环境**: 使用分步骤生成，便于调试和测试
2. **生产环境**: 可以根据需求选择完整管道或分步骤生成
3. **批量处理**: 建议使用客户端脚本
4. **实时应用**: 使用流式文本生成提供更好的用户体验 