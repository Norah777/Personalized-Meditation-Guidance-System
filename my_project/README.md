# Peace Processor Pipeline

基於 Azure OpenAI Service 的文本、圖像和視頻生成管道

## 環境設置

1. 複製 `.env.example` 文件並重命名為 `.env`：

```bash
cp .env.example .env
```

2. 編輯 `.env` 文件，填入你的 Azure OpenAI Service 憑證：

```env
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
```

3. 如果你的 Azure OpenAI 部署名稱與模型名稱不同，請在 `.env` 文件中修改相應的部署名稱：

```env
AZURE_OPENAI_GPT4O_DEPLOYMENT=your_gpt4o_deployment_name
AZURE_OPENAI_DALLE3_DEPLOYMENT=your_dalle3_deployment_name
AZURE_OPENAI_TTS1_DEPLOYMENT=your_tts1_deployment_name
```

## 依賴安裝

安裝所需的依賴：

```bash
pip install -r requirements.txt
```

## 測試 Azure OpenAI API

運行測試腳本來驗證你的 Azure OpenAI API 配置是否正常工作：

```bash
python test_azure.py
```

測試腳本將測試三個主要功能：
- 文本生成 (GPT-4o / GPT-3.5-Turbo)
- 圖像生成 (DALL-E 3)
- 文本轉語音 (TTS-1)

你可以使用命令行參數選擇性地跳過某些測試：

```bash
# 跳過圖像生成測試
python test_azure.py --skip_image

# 僅運行文本生成測試
python test_azure.py --skip_image --skip_speech

# 使用命令行提供的 API 密鑰和端點
python test_azure.py --api_key YOUR_API_KEY --api_base YOUR_ENDPOINT
```

測試結果將保存在 `test_output` 目錄中。

## 運行管道

完整管道可以通過 `main.py` 運行：

```bash
python main.py --user_prompt "我想要一個關於森林中冥想的指導" --emotional_state "放鬆"
```

參數解釋：
- `--user_prompt`: 用戶輸入的提示詞
- `--emotional_state`: 用戶的情緒狀態
- `--output_path`: 輸出文件的保存路徑（默認為 "output"） 