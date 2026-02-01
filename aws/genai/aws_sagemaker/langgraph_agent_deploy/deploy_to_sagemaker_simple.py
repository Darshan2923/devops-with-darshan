"""
Simple SageMaker Deployment Script using boto3 directly

This script deploys a Docker image to Amazon SageMaker without using the SageMaker SDK.
"""

import boto3
from datetime import datetime
import json

# Configuration
AWS_REGION = "us-east-1"
ECR_REPOSITORY_NAME = "langgraph-bedrock-agent"
MODEL_NAME = f"langgraph-agent-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
ENDPOINT_NAME = f"langgraph-endpoint-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
EXECUTION_ROLE = "your-execution-role-arn-here"

# Initialize AWS clients
session = boto3.Session(region_name=AWS_REGION)
sagemaker_client = session.client('sagemaker')
ecr_client = session.client('ecr')
sts_client = session.client('sts')

# Get account ID
account_id = sts_client.get_caller_identity()['Account']
image_uri = f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/{ECR_REPOSITORY_NAME}:latest"

print("="*60)
print("SageMaker Deployment Script")
print("="*60)
print(f"Region: {AWS_REGION}")
print(f"Account: {account_id}")
print(f"Image URI: {image_uri}")
print(f"Execution Role: {EXECUTION_ROLE}")
print("="*60)
print()

# Step 1: Create Model
print("Step 1: Creating SageMaker Model...")
try:
    model_response = sagemaker_client.create_model(
        ModelName=MODEL_NAME,
        PrimaryContainer={
            'Image': image_uri,
            'Mode': 'SingleModel',
            'Environment': {
                'OPENROUTER_API_KEY': 'placeholder',  # Set this via endpoint config
            }
        },
        ExecutionRoleArn=EXECUTION_ROLE
    )
    print(f"✅ Model created: {MODEL_NAME}")
    print(f"   ARN: {model_response['ModelArn']}")
except Exception as e:
    print(f"❌ Failed to create model: {e}")
    exit(1)

# Step 2: Create Endpoint Configuration
print("\nStep 2: Creating Endpoint Configuration...")
endpoint_config_name = f"{MODEL_NAME}-config"
try:
    config_response = sagemaker_client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[
            {
                'VariantName': 'AllTraffic',
                'ModelName': MODEL_NAME,
                'InitialInstanceCount': 1,
                'InstanceType': 'ml.m5.xlarge',
                'InitialVariantWeight': 1.0
            }
        ]
    )
    print(f"✅ Endpoint config created: {endpoint_config_name}")
    print(f"   ARN: {config_response['EndpointConfigArn']}")
except Exception as e:
    print(f"❌ Failed to create endpoint config: {e}")
    exit(1)

# Step 3: Create Endpoint
print("\nStep 3: Creating Endpoint (this may take 5-10 minutes)...")
try:
    endpoint_response = sagemaker_client.create_endpoint(
        EndpointName=ENDPOINT_NAME,
        EndpointConfigName=endpoint_config_name
    )
    print(f"✅ Endpoint creation initiated: {ENDPOINT_NAME}")
    print(f"   ARN: {endpoint_response['EndpointArn']}")
    print("\n⏳ Waiting for endpoint to be in service...")
    
    # Wait for endpoint to be ready
    waiter = sagemaker_client.get_waiter('endpoint_in_service')
    waiter.wait(EndpointName=ENDPOINT_NAME)
    
    print(f"\n🎉 Endpoint is now in service!")
    print(f"   Endpoint Name: {ENDPOINT_NAME}")
    
except Exception as e:
    print(f"❌ Failed to create endpoint: {e}")
    exit(1)

# Step 4: Test the endpoint
print("\nStep 4: Testing endpoint...")
runtime_client = session.client('sagemaker-runtime')

test_payload = {
    "bucket": "my-langgraph-bedrock-agent",
    "input_key": "input/input.txt",
    "output_key": "output/output.txt"
}

try:
    response = runtime_client.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType='application/json',
        Body=json.dumps(test_payload)
    )
    
    result = json.loads(response['Body'].read().decode())
    print(f"✅ Test successful!")
    print(f"   Response: {result}")
except Exception as e:
    print(f"⚠️  Test failed (endpoint may need time to warm up): {e}")

print("\n" + "="*60)
print("Deployment Complete!")
print("="*60)
print(f"Endpoint Name: {ENDPOINT_NAME}")
print(f"Model Name: {MODEL_NAME}")
print(f"Region: {AWS_REGION}")
print("\nTo invoke the endpoint:")
print(f"aws sagemaker-runtime invoke-endpoint \\")
print(f"  --endpoint-name {ENDPOINT_NAME} \\")
print(f"  --content-type application/json \\")
print(f"  --body '{{\"bucket\":\"my-langgraph-bedrock-agent\",\"input_key\":\"input/input.txt\",\"output_key\":\"output/output.txt\"}}' \\")
print(f"  output.json")
print("\nTo delete the endpoint when done:")
print(f"aws sagemaker delete-endpoint --endpoint-name {ENDPOINT_NAME}")
print(f"aws sagemaker delete-endpoint-config --endpoint-config-name {endpoint_config_name}")
print(f"aws sagemaker delete-model --model-name {MODEL_NAME}")
print("="*60)
