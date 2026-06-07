# AWS Deployment Guide - Resume Analyzer

This guide walks you through deploying the Resume Analyzer to AWS using multiple service options.

## 📋 Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured (`aws configure`)
- Docker installed locally
- kubectl installed (for EKS)
- Terraform installed (optional, for Infrastructure as Code)

## 🚀 Deployment Options

### Option 1: ECS (Elastic Container Service) - RECOMMENDED ⭐
- **Best for**: Quick setup, cost-effective, managed containers
- **Time**: ~15 minutes
- **Cost**: ~$5-15/month (with free tier eligibility)

### Option 2: EKS (Elastic Kubernetes Service)
- **Best for**: Production-grade, complex orchestration
- **Time**: ~30 minutes
- **Cost**: ~$73/month (cluster fee) + compute

### Option 3: EC2 (Manual)
- **Best for**: Full control, learning
- **Time**: ~20 minutes
- **Cost**: ~$5-20/month (t3.micro eligible for free tier)

### Option 4: AppRunner (Serverless)
- **Best for**: Simplest deployment, auto-scaling
- **Time**: ~5 minutes
- **Cost**: ~$7/month + per-request pricing

---

## 🎯 Quick Start: ECS Fargate (Recommended)

```bash
# 1. Configure AWS
aws configure

# 2. Build and push Docker image
cd aws/scripts
bash build-and-push.sh latest

# 3. Deploy with CloudFormation
cd ../cloudformation
bash deploy-stack.sh YOUR_IMAGE_URI

# 4. Monitor deployment
cd ../scripts
bash monitor-service.sh
```

---

## 📊 Cost Comparison

| Option | Monthly Cost | Setup Time | Best For |
|--------|-------------|-----------|----------|
| ECS | $90-120 | 15 min | Production-ready, cost-effective |
| EKS | $115-130 | 30 min | Complex, multi-service |
| EC2 | $15-30 | 20 min | Learning, full control |
| AppRunner | $37-57 | 5 min | Simplest, auto-scaling |

**💰 FREE TIER: First 12 months can be completely free with AWS free tier!**

---

## 📁 Directory Structure

```
aws/
├── README.md                          # This file
├── cost-estimation.md                 # Detailed cost breakdown
├── ecs/                               # ECS deployment configs
│   ├── task-definition.json
│   ├── task-role-trust-policy.json
│   └── ecs-service-policy.json
├── eks/                               # EKS deployment configs
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── hpa.yaml
├── ec2/                               # EC2 deployment scripts
│   ├── user-data.sh
│   └── security-group.sh
├── rds/                               # RDS database setup
│   └── create-db.sh
├── apprunner/                         # AppRunner configs
│   ├── source-config.json
│   └── apprunner.yaml
├── lambda/                            # AWS Lambda functions
│   ├── handler.py
│   └── requirements.txt
├── cloudformation/                    # Infrastructure as Code
│   ├── resume-analyzer-stack.yaml
│   └── deploy-stack.sh
├── terraform/                         # Terraform IaC
│   ├── main.tf
│   ├── variables.tf
│   └── terraform.tfvars
├── monitoring/                        # CloudWatch configs
│   ├── cloudwatch-dashboard.json
│   └── alarms.sh
├── scripts/                           # Helper scripts
│   ├── build-and-push.sh
│   ├── deploy-ecs-service.sh
│   └── monitor-service.sh
└── ci-cd/                             # GitHub Actions
    └── .github/workflows/deploy-to-aws.yaml
```

---

## 🎯 Option 1: ECS Fargate (FASTEST - 15 minutes)

### Step 1: Create ECR Repository

```bash
AWS_REGION=us-east-1
aws ecr create-repository --repository-name resume-analyzer --region $AWS_REGION
```

### Step 2: Build and Push Image

```bash
cd aws/scripts
bash build-and-push.sh latest
```

### Step 3: Deploy with CloudFormation

```bash
IMAGE_URI="YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/resume-analyzer:latest"
cd ../cloudformation
bash deploy-stack.sh $IMAGE_URI
```

### Step 4: Get Load Balancer URL

```bash
aws cloudformation describe-stacks \
  --stack-name resume-analyzer-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' \
  --output text
```

Access your app at: `http://YOUR_ALB_DNS`

---

## 🎯 Option 2: EKS (Production-Grade)

### Step 1: Create Cluster

```bash
exsctl create cluster \
  --name resume-analyzer \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 2
```

### Step 2: Deploy Application

```bash
kubectl create namespace resume-analyzer
kubectl apply -f aws/eks/configmap.yaml -n resume-analyzer
kubectl apply -f aws/eks/deployment.yaml -n resume-analyzer
kubectl apply -f aws/eks/service.yaml -n resume-analyzer
kubectl apply -f aws/eks/hpa.yaml -n resume-analyzer
```

### Step 3: Access Application

```bash
kubectl get svc -n resume-analyzer
# Use the LoadBalancer EXTERNAL-IP
```

---

## 🎯 Option 3: EC2 (Simplest Learning Option)

### Step 1: Create Security Group

```bash
bash aws/ec2/security-group.sh
```

### Step 2: Launch EC2 Instance

```bash
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name your-key-pair \
  --security-groups resume-analyzer-sg \
  --user-data file://aws/ec2/user-data.sh
```

### Step 3: Get IP and Access

```bash
aws ec2 describe-instances --query 'Reservations[0].Instances[0].PublicIpAddress'
# Access at: http://YOUR_IP:5000
```

---

## 🎯 Option 4: AppRunner (Easiest)

```bash
# Update ACCOUNT_ID in source-config.json
aws apprunner create-service \
  --service-name resume-analyzer \
  --source-configuration file://aws/apprunner/source-config.json
```

---

## 🔐 Setup with Database (RDS)

```bash
bash aws/rds/create-db.sh YourSecurePassword123!
```

Add the connection string to your environment variables.

---

## 📊 Monitoring & Logging

### View Logs (ECS)
```bash
aws logs tail /ecs/resume-analyzer --follow
```

### Create CloudWatch Dashboard
```bash
aws cloudwatch put-dashboard \
  --dashboard-name resume-analyzer \
  --dashboard-body file://aws/monitoring/cloudwatch-dashboard.json
```

### Create Alarms
```bash
bash aws/monitoring/alarms.sh
```

---

## 🔄 CI/CD with GitHub Actions

1. Set GitHub secrets:
   - `AWS_ACCOUNT_ID`
   - `AWS_ROLE_TO_ASSUME` (optional for OIDC)

2. GitHub Actions will auto-deploy on push to main:
   ```bash
   git push origin main
   ```

---

## 🛠️ Infrastructure as Code

### Using Terraform

```bash
cd aws/terraform
terraform init
terraform plan
terraform apply
```

### Using CloudFormation

```bash
cd aws/cloudformation
bash deploy-stack.sh YOUR_IMAGE_URI
```

---

## 💡 Cost Optimization

1. **Auto-Scaling**: Enable target tracking for 30-50% savings
2. **Reserved Instances**: 40-70% discount with 1-3 year commitment
3. **Spot Instances**: Up to 70% discount for non-critical workloads
4. **CloudFront**: Cache assets, reduce bandwidth
5. **Free Tier**: Use t2.micro for 12 months free!

---

## 🔗 Links & Resources

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/)
- [AWS AppRunner Documentation](https://docs.aws.amazon.com/apprunner/)
- [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)

---

## ✅ Deployment Checklist

- [ ] AWS Account created and configured
- [ ] AWS CLI installed and configured
- [ ] Docker installed
- [ ] Repository code cloned
- [ ] Deployment option chosen
- [ ] Docker image built and pushed
- [ ] Infrastructure deployed
- [ ] Application accessible
- [ ] Monitoring configured
- [ ] CI/CD pipeline set up (optional)

---

## 📞 Support & Troubleshooting

### Task won't start
```bash
aws ecs describe-tasks --cluster resume-analyzer-cluster --tasks TASK_ARN
```

### Check logs
```bash
aws logs tail /ecs/resume-analyzer --follow
```

### Database connection issues
```bash
aws rds describe-db-instances --db-instance-identifier resume-analyzer-db
```

---

**Happy deploying! 🚀**

For questions or issues, check the AWS documentation or open an issue on GitHub.
