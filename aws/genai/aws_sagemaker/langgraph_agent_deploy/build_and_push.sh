#!/bin/bash

# Build and Push Docker Image to ECR
# This script automates Docker image creation and pushing to Amazon ECR

set -e  # Exit on error

# Configuration
AWS_REGION="us-east-1"
ECR_REPOSITORY_NAME="langgraph-bedrock-agent"
IMAGE_TAG="latest"

echo "=== Docker Build & Push Script ==="
echo ""

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "✓ AWS Account ID: $ACCOUNT_ID"

# Create ECR repository if it doesn't exist
echo ""
echo "Creating ECR repository (if it doesn't exist)..."
aws ecr describe-repositories --repository-names ${ECR_REPOSITORY_NAME} --region ${AWS_REGION} 2>/dev/null || \
    aws ecr create-repository --repository-name ${ECR_REPOSITORY_NAME} --region ${AWS_REGION}
echo "✓ ECR repository ready: ${ECR_REPOSITORY_NAME}"

# ECR image URI
ECR_IMAGE_URI="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:${IMAGE_TAG}"

# Login to ECR
echo ""
echo "Logging in to ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
echo "✓ Logged in to ECR"

# Build Docker image
echo ""
echo "Building Docker image for SageMaker (linux/amd64)..."
docker build --platform linux/amd64 -t ${ECR_REPOSITORY_NAME}:${IMAGE_TAG} .
echo "✓ Docker image built: ${ECR_REPOSITORY_NAME}:${IMAGE_TAG}"

# Tag image for ECR
echo ""
echo "Tagging image for ECR..."
docker tag ${ECR_REPOSITORY_NAME}:${IMAGE_TAG} ${ECR_IMAGE_URI}
echo "✓ Image tagged: ${ECR_IMAGE_URI}"

# Push to ECR
echo ""
echo "Pushing image to ECR..."
docker push ${ECR_IMAGE_URI}
echo "✓ Image pushed to ECR"

echo ""
echo "=== Build & Push Complete ==="
echo "Image URI: ${ECR_IMAGE_URI}"
echo ""
echo "Next step: Update deploy_to_sagemaker.py with your SageMaker execution role ARN"
echo "Then run: python deploy_to_sagemaker.py"
