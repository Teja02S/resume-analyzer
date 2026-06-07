# AWS Cost Estimation - Resume Analyzer

## Monthly Cost Breakdown

### Option 1: ECS on Fargate (Recommended)

**Compute:**
- Task: 256 CPU, 512 MB memory
- Replicas: 2-3 running 24/7
- Fargate pricing: $0.04048 per vCPU-hour + $0.00445 per GB-hour
- **Monthly: ~$60-90**

**Load Balancer (ALB):**
- ALB: $16.20/month
- LCU: ~$5-10/month
- **Monthly: ~$20-25**

**CloudWatch Logs:**
- $0.50 per GB ingested
- **Monthly: ~$5-10**

**TOTAL: $90-120/month**

### Option 2: EKS
- EKS Control: $73/month
- EC2 Compute: ~$30-50/month
- **TOTAL: $115-130/month**

### Option 3: EC2 (t3.micro)
- t3.micro: ~$8.50/month (FREE with free tier!)
- EBS: ~$2/month
- **TOTAL: $10-20/month**

### Option 4: AppRunner
- Base: $7/month
- Compute: ~$30-50/month
- **TOTAL: $37-57/month**

## 💰 AWS Free Tier

**Services included (12 months):**
- EC2: 750 hours/month of t2.micro
- CloudWatch: 5 GB logs
- ECS: Free (pay for compute)

**First-time AWS users: COMPLETELY FREE for 12 months!**
