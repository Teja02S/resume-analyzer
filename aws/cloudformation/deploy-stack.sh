#!/bin/bash
set -e

STACK_NAME="resume-analyzer-stack"
TEMPLATE_FILE="resume-analyzer-stack.yaml"
REGION="us-east-1"
IMAGE_URI="$1"

if [ -z "$IMAGE_URI" ]; then
  echo "Usage: ./deploy-stack.sh <IMAGE_URI>"
  echo "Example: ./deploy-stack.sh 123456789.dkr.ecr.us-east-1.amazonaws.com/resume-analyzer:latest"
  exit 1
fi

echo "Deploying CloudFormation stack..."

aws cloudformation deploy \
  --template-file $TEMPLATE_FILE \
  --stack-name $STACK_NAME \
  --parameter-overrides ImageUri=$IMAGE_URI EnvironmentName=production DesiredCount=2 \
  --capabilities CAPABILITY_IAM \
  --region $REGION

echo "Stack deployment completed!"
