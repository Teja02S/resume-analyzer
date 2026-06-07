#!/bin/bash
set -e

yum update -y
amazon-linux-extras install docker -y
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user

curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

yum install -y git

cd /home/ec2-user
git clone https://github.com/Teja02S/resume-analyzer.git
cd resume-analyzer

cat > .env <<EOF
FLASK_ENV=production
DEBUG=False
SECRET_KEY=$(openssl rand -hex 32)
EOF

docker-compose up -d

echo "Resume Analyzer deployed successfully!"
echo "Access at: http://$(ec2-metadata --public-ipv4 | cut -d ' ' -f 2):5000"
