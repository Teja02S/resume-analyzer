#!/bin/bash

CLUSTER_NAME="resume-analyzer-cluster"
SERVICE_NAME="resume-analyzer-service"
REGION="${AWS_REGION:-us-east-1}"

echo "Monitoring Resume Analyzer ECS Service"
echo "======================================="
echo ""

echo "Service Status:"
aws ecs describe-services \
  --cluster $CLUSTER_NAME \
  --services $SERVICE_NAME \
  --region $REGION \
  --query 'services[0].{ServiceName:serviceName,Status:status,RunningCount:runningCount,DesiredCount:desiredCount}' \
  --output table

echo ""
echo "Recent Logs:"
aws logs tail /ecs/resume-analyzer --follow --since 5m
