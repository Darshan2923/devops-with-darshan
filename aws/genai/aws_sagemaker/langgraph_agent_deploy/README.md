# LangGraph S3 Processing Agent 🚀

Process text files from S3 using LangGraph and OpenRouter LLMs, then save results back to S3.

## 🎯 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set OpenRouter API Key
Get your free API key from [https://openrouter.ai/keys](https://openrouter.ai/keys)

```bash
# Windows
set OPENROUTER_API_KEY=your-key-here

# Linux/Mac
export OPENROUTER_API_KEY=your-key-here
```

### 3. Run Locally
```bash
python test_locally.py
```

## 📋 What It Does

1. **Reads** `input/input.txt` from S3 bucket `my-langgraph-bedrock-agent`
2. **Processes** text using Claude 3.5 Sonnet via OpenRouter
3. **Writes** summary to `output/output.txt` in the same S3 bucket

## 📁 Project Structure

```
langgraph_agent_deploy/
├── agent_graph.py              # Main LangGraph workflow
├── app.py                      # FastAPI server
├── test_locally.py             # Local testing script
├── Dockerfile                  # Container definition
├── requirements.txt            # Python dependencies
├── deploy_to_sagemaker.py      # SageMaker deployment
├── build_and_push.sh           # ECR build script
├── DEPLOYMENT_GUIDE.md         # Full deployment guide
├── OPENROUTER_SETUP.md         # OpenRouter setup guide
└── README.md                   # This file
```

## 🐳 Docker Deployment

### Build & Run Locally
```bash
docker build -t langgraph-agent:latest .
docker run -p 8080:8080 \
  -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  langgraph-agent:latest
```

### Test Container
```bash
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "bucket": "my-langgraph-bedrock-agent",
    "input_key": "input/input.txt",
    "output_key": "output/output.txt"
  }'
```

## ☁️ SageMaker Deployment

### 1. Build & Push to ECR
```bash
./build_and_push.sh
```

### 2. Deploy to SageMaker
```bash
python deploy_to_sagemaker.py
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 🔑 Configuration

### Environment Variables
- `OPENROUTER_API_KEY` - Your OpenRouter API key (required)
- `AWS_REGION` - AWS region (default: us-east-1)
- `AWS_ACCESS_KEY_ID` - AWS credentials (optional if using IAM role)
- `AWS_SECRET_ACCESS_KEY` - AWS credentials (optional if using IAM role)

### Change LLM Model
Edit [agent_graph.py](agent_graph.py) line 49:

```python
"model": "anthropic/claude-3.5-sonnet",  # Change this
```

**Free models:**
- `meta-llama/llama-3.1-8b-instruct:free`
- `google/gemma-2-9b-it:free`

See all models: https://openrouter.ai/models

## 📚 Documentation

- **[OPENROUTER_SETUP.md](OPENROUTER_SETUP.md)** - OpenRouter configuration and troubleshooting
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment guide for AWS

## 🐛 Troubleshooting

### API Key Not Set
```
⚠️  WARNING: OPENROUTER_API_KEY not set!
```
**Fix:** Set the environment variable as shown in Quick Start

### S3 Access Denied
**Fix:** Ensure your AWS credentials have S3 read/write permissions

### OpenRouter Rate Limit
**Fix:** Wait or upgrade to paid tier at https://openrouter.ai

## 💰 Cost Estimate

- **OpenRouter (Claude 3.5)**: ~$3-15 per 1M tokens
- **S3**: $0.023 per GB/month + requests
- **SageMaker (ml.m5.xlarge)**: ~$0.23/hour

**Free tier available** for testing with free models!

## 🎓 Learn More

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [OpenRouter Docs](https://openrouter.ai/docs)
- [AWS SageMaker Docs](https://docs.aws.amazon.com/sagemaker/)

## 📝 License

MIT

---

**Need help?** Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) or [OPENROUTER_SETUP.md](OPENROUTER_SETUP.md)
