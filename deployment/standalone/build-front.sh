#!/bin/bash

# Configuration
AWS_REGION="us-east-1"
ECR_REPO_NAME="chatbot/api"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Environment-specific configurations
case "$1" in
  "dev")
    ENV="dev"
    API_URL="http://chatbot-app.chatbot-dev.svc.cluster.local"
    ;;
  "prod")
    ENV="prod"
    API_URL="http://chatbot-app.chatbot-prod.svc.cluster.local"
    ;;
  *)
    echo "Usage: $0 {dev|prod}"
    exit 1
    ;;
esac

# Set the full repository URI
ECR_REPO_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"

echo "Building and pushing frontend image for ${ENV} environment..."

# Login to ECR
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO_URI}

# Build the Docker image
docker build -f $(pwd)/../../frontend/Dockerfile -t ${ECR_REPO_NAME} $(pwd)/../../frontend
IMAGE_TAG="latest"

docker tag ${ECR_REPO_NAME}:${IMAGE_TAG} ${ECR_REPO_URI}:${IMAGE_TAG}

# Push the images
docker push ${ECR_REPO_URI}:${IMAGE_TAG}

echo "Frontend image built and pushed successfully!"