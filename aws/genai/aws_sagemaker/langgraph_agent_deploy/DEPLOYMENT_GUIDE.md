# LangGraph Bedrock Agent - Deployment Guide

## Overview
This project processes text from S3 using AWS Bedrock and LangGraph, then saves the results back to S3.

## Architecture
1. **S3 Reader Agent**: Reads `input/input.txt` from S3
2. **OpenRouter LLM Agent**: Processes text using Claude 3.5 Sonnet (via OpenRouter)
3. **S3 Writer Agent**: Writes result to `output/output.txt` in S3

## Prerequisites

### API Keys
- **OpenRouter API Key**: Get from [https://openrouter.ai/keys](https://openrouter.ai/keys)
  - Sign up and create an API key
  - Free tier available with rate limits
  - Paid models for production use

### AWS Resources
- **S3 Bucket**: `s3://my-langgraph-bedrock-agent/`
  - `/input/input.txt` - Input file
  - `/output/` - Output folder (empty initially)

### AWS Permissions Required
- **S3**: `s3:GetObject`, `s3:PutObject`
- **ECR**: `ecr:*` (for Docker image storage)
- **SageMaker**: Full access for deployment

**Note**: No longer requires AWS Bedrock permissions - using OpenRouter instead!

### Local Requirements
- Python 3.10+
- Docker
- AWS CLI configured with credentials
- Boto3 with AWS credentials

## Setup

### 1. Install Dependencies
```bash
cd langgraph_agent_deploy
pip install -r requirements.txt
```

### 2. Configure AWS Credentials
Ensure your AWS credentials are configured:
```bash
aws configure
```
Set OpenRouter API Key
Get your API key from [https://openrouter.ai/keys](https://openrouter.ai/keys), then:

**Windows:**
```cmd
set OPENROUTER_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export OPENROUTER_API_KEY=your-api-key-here
Make sure `OPENROUTER_API_KEY` is set, then:
```bash
python test_locally.py
```

This will:
1. Read from `s3://my-langgraph-bedrock-agent/input/input.txt`
2. Process with OpenRouter (Claude 3.5 Sonnet)cument that needs to be processed and summarized." > input.txt
aws s3 cp input.txt s3://my-langgraph-bedrock-agent/input/input.txt
```

## Local Testing

### Test the Agent Graph Locally
```bash
python test_locally.py
```

This will:
1. Read from `s3://my-langgraph-bedrock-agent/input/input.txt`
2. Process with Bedrock
3. Write to `s3://my-langgraph-bedrock-agent/output/output.txt`

### Test the FastAPI Server Locally
```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

Then in another terminal:
```bash
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{nd OpenRouter key are available)
docker run -p 8080:8080 \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
  -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY
```

## Docker Deployment

### Build and Test Docker Image Locally
```bash
# Build image
docker build -t langgraph-bedrock-agent:latest .

# Run container (make sure AWS credentials are available)
docker run -p 8080:8080 \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
  langgraph-bedrock-agent:latest

# Test the container
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "bucket": "my-langgraph-bedrock-agent",
    "input_key": "input/input.txt",
    "output_key": "output/output.txt"
  }'
```

## SageMaker Deployment

### Step 1: Build and Push to ECR

#### Option A: Using the Shell Script (Linux/Mac/Git Bash)
```bash
chmod +x build_and_push.sh
./build_and_push.sh
```

#### Option B: Manual Commands (Windows/PowerShell)
```powershell
# Set variables
$AWS_REGION = "us-east-1"
$ECR_REPOSITORY_NAME = "langgraph-bedrock-agent"
$ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)

# Create ECR repository
aws ecr create-repository --repository-name $ECR_REPOSITORY_NAME --region $AWS_REGION

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# Build and push
docker build -t ${ECR_REPOSITORY_NAME}:latest .
docker tag ${ECR_REPOSITORY_NAME}:latest "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/${ECR_REPOSITORY_NAME}:latest"
docker push "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/${ECR_REPOSITORY_NAME}:latest"
```

### Step 2: Deploy to SageMaker

1. **Create SageMaker Execution Role** (if you don't have one):
   - Go to IAM Console
   - Create a new role for SageMaker
   - Attach policies:
     - `AmazonSageMakerFullAccess`
     - `AmazonS3FullAccess`
     - `AmazonBedrockFullAccess`
   - Copy the Role ARN

2. **Update `deploy_to_sagemaker.py`**:
   - Replace `YOUR_SAGEMAKER_EXECUTION_ROLE_ARN` with your role ARN

3. **Run the deployment script**:
```bash
python deploy_to_sagemaker.py
```

### Step 3: Test SageMaker Endpoint

```python
import boto3
import json

runtime_client = boto3.client('sagemaker-runtime', region_name='us-east-1')

payload = {
    "bucket": "my-langgraph-bedrock-agent",
    "input_key": "input/input.txt",
    "output_key": "output/output.txt"
}

response = runtime_client.invoke_endpoint(
    EndpointName='YOUR_ENDPOINT_NAME',  # Get from deployment output
    ContentType='application/json',
    Body=json.dumps(payload)
)

result = json.loads(response['Body'].read().decode())
print(result)
```

## Verify Results

Check the output in S3:
```bash
aws s3 cp s3://my-langgraph-bedrock-agent/output/output.txt -
```

## Troubleshooting

### COpenRouter API Key Not Set**
   - Verify key is set: `echo $OPENROUTER_API_KEY`
   - Get key from: https://openrouter.ai/keys
   - See OPENROUTER_SETUP.md for details

2. **OpenRouter Rate Limiting**
   - Ensure IAM permissions for S3 read/write
   - Check bucket policy

4  - Check model access in Bedrock console

2. **Check internet connection for pip installs
   - Verify requirements.txt is present

5
3. **Docker Build Fails**
   - Ensure Docker is running
   - Check internet connection for pip installs
   - Verify requirements.txt is present

4. **SageMaker Deployment Fails**
   - Verify execution role ARN is correct
   - Ensure role has necessary permissions
   - Check ECR image was pushed successfully
   - Verify instance type availability in your region

### Logs

- **Local testing**: Output in terminal
- **Docker**: `docker logs <container_id>`
- **SageMaker**: Check CloudWatch Logs in AWS Console

## Clean Up

### Delete SageMaker Endpoint
```bash
aws sagemaker delete-endpoint --endpoint-name YOUR_ENDPOINT_NAME
aws sagemaker delete-endpoint-config --endpoint-config-name YOUR_ENDPOINT_CONFIG_NAME
aws sagemaker delete-model --model-name YOUR_MODEL_NAME
```

### Delete ECR Repository
```bash
aws ecr delete-repository --repository-name langgraph-bedrock-agent --force --region us-east-1
```
OpenRouter**: Variable by model (free tier available, see OPENROUTER_SETUP.md)
## Cost Considerations

- **SageMaker**: ml.m5.xlarge instance (~$0.23/hour)
- **Bedrock**: Claude 3 Sonnet pricing per token
- **S3**: Minimal storage and request costs
- **ECR**: Storage for Docker images

Remember to delete resources when not in use to avoid (S3→OpenRouter→S3)
- `app.py` - FastAPI application
- `test_locally.py` - Local testing script
- `Dockerfile` - Container definition
- `requirements.txt` - Python dependencies
- `build_and_push.sh` - ECR build/push automation
- `deploy_to_sagemaker.py` - SageMaker deployment script
- `DEPLOYMENT_GUIDE.md` - This file
- `OPENROUTER_SETUP.md` - OpenRouter configuration guidion
- `requirements.txt` - Python dependencies
- `build_and_push.sh` - ECR build/push automation
- `deploy_to_sagemaker.py` - SageMaker deployment script
- `DEPLOYMENT_GUIDE.md` - This file
