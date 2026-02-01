# Quick Setup Guide - OpenRouter Integration

## What Changed?

Replaced AWS Bedrock with **OpenRouter** to avoid throttling issues and provide more flexibility with model selection.

## Setup Steps

### 1. Get OpenRouter API Key

1. Go to [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign up or log in
3. Create a new API key
4. Copy your API key

### 2. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:OPENROUTER_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENROUTER_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

Or use the provided scripts:
- Windows: `set_env.bat`
- Linux/Mac: `source set_env.sh`

### 3. Test Locally

```bash
python test_locally.py
```

## Available Models

The code is configured to use `anthropic/claude-3.5-sonnet`. You can change this in [agent_graph.py](agent_graph.py#L49) to:

### Free Models:
- `meta-llama/llama-3.1-8b-instruct:free`
- `google/gemma-2-9b-it:free`
- `microsoft/phi-3-mini-128k-instruct:free`

### Paid Models:
- `anthropic/claude-3.5-sonnet` (recommended)
- `anthropic/claude-3-opus`
- `openai/gpt-4-turbo`
- `google/gemini-pro-1.5`

See all models at: https://openrouter.ai/models

## Docker Deployment

When building Docker image, pass the API key:

```bash
docker build --build-arg OPENROUTER_API_KEY=your-key -t langgraph-bedrock-agent:latest .
```

Or set it at runtime:

```bash
docker run -e OPENROUTER_API_KEY=your-key -p 8080:8080 langgraph-bedrock-agent:latest
```

## SageMaker Deployment

When deploying to SageMaker, set the environment variable in the deployment script or pass it through SageMaker environment configuration.

## Cost Considerations

OpenRouter pricing varies by model:
- **Free models**: $0 (rate limited)
- **Claude 3.5 Sonnet**: ~$3 per 1M input tokens, ~$15 per 1M output tokens
- Check current pricing: https://openrouter.ai/models

## Troubleshooting

### API Key Not Set
```
⚠️  WARNING: OPENROUTER_API_KEY not set!
```
**Solution**: Set the environment variable as shown above.

### API Rate Limiting
```
Error: 429 Too Many Requests
```
**Solution**: 
- Wait a moment and retry
- Use a different model
- Check your OpenRouter account credits

### Network Error
```
Error: Connection timeout
```
**Solution**:
- Check internet connection
- Verify firewall settings
- Try increasing timeout in agent_graph.py (line 55)

## Architecture Update

**Old Flow:**
S3 → Bedrock (Claude) → S3

**New Flow:**
S3 → OpenRouter (Claude/any model) → S3

Benefits:
- ✅ No AWS Bedrock throttling
- ✅ Access to multiple model providers
- ✅ Free model options available
- ✅ Easier to test locally
- ✅ More cost control
