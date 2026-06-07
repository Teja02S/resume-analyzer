#!/bin/bash
set -e

REGION="${AWS_REGION:-us-east-1}"
REPO_NAME="resume-analyzer"
GIT_SHA=$(git rev-parse --short HEAD)
IMAGE_TAG="${1:-latest}"

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"
ECR_REPOSITORY="$ECR_REGISTRY/$REPO_NAME"

echo "Building and pushing Docker image..."
echo "Registry: $ECR_REGISTRY"
echo "Repository: $ECR_REPOSITORY"
echo "Tag: $IMAGE_TAG"

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

docker build -t $REPO_NAME:$IMAGE_TAG -t $ECR_REPOSITORY:$IMAGE_TAG -t $ECR_REPOSITORY:$GIT_SHA .

docker push $ECR_REPOSITORY:$IMAGE_TAG
docker push $ECR_REPOSITORY:$GIT_SHA

echo "Successfully pushed images:"
echo "  - $ECR_REPOSITORY:$IMAGE_TAG"
echo "  - $ECR_REPOSITORY:$GIT_SHA"
echo ""
echo "Image URI: $ECR_REPOSITORY:$IMAGE_TAG"
