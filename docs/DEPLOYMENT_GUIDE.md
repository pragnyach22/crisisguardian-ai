# CrisisGuardian AI - Deployment Guide

## Overview

This guide covers deploying CrisisGuardian AI to production environments including local deployment, Docker, and cloud platforms.

## Prerequisites

- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`
- Git
- API Keys: Google Gemini API, OpenWeatherMap (optional)

## Local Deployment

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/crisisguardian-ai/crisisguardian-ai.git
cd crisisguardian-ai

# Create .env from template
cp .env.template .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

### 2. Install Dependencies

Using `uv` (recommended):
```bash
uv sync
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Run Backend API

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 4. Run Frontend (in another terminal)

```bash
streamlit run frontend/app.py
```

The frontend will be available at `http://localhost:8501`

### 5. Verify Deployment

```bash
# Health check
curl http://localhost:8000/health

# Expected response
{"status": "healthy", "service": "CrisisGuardian AI"}
```

---

## Docker Deployment

### 1. Build Docker Image

```bash
docker build -t crisisguardian-ai:latest .
```

### 2. Run Container

```bash
docker run -e GEMINI_API_KEY=your_key_here \
           -p 8000:8000 \
           -p 8501:8501 \
           crisisguardian-ai:latest
```

### 3. Docker Compose (Recommended)

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - BACKEND_HOST=0.0.0.0
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
  
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
    depends_on:
      - backend
```

Run with:
```bash
docker-compose up -d
```

---

## Cloud Deployment

### Google Cloud Run

```bash
# Build and push to Cloud Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/crisisguardian-ai

# Deploy
gcloud run deploy crisisguardian-ai \
  --image gcr.io/PROJECT_ID/crisisguardian-ai \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=your_key_here
```

### AWS ECS

```bash
# Create ECR repository
aws ecr create-repository --repository-name crisisguardian-ai

# Build and push
docker build -t crisisguardian-ai:latest .
docker tag crisisguardian-ai:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/crisisguardian-ai:latest
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/crisisguardian-ai:latest
```

### Azure Container Instances

```bash
# Create resource group
az group create --name crisisguardian-rg --location eastus

# Deploy
az container create \
  --resource-group crisisguardian-rg \
  --name crisisguardian-ai \
  --image crisisguardian-ai:latest \
  --port 8000 8501 \
  --environment-variables GEMINI_API_KEY=your_key_here
```

---

## Production Configuration

### 1. Environment Variables

```bash
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# API Keys
GEMINI_API_KEY=your_production_key_here
OPENWEATHER_API_KEY=your_key_here

# Logging
LOG_LEVEL=WARNING
LOG_FILE=/var/log/crisisguardian/app.log

# Security
API_CORS_ORIGINS=["https://yourdomain.com"]

# Features
ENABLE_MOCK_DATA=false
ENABLE_DETAILED_LOGGING=false
```

### 2. Logging Configuration

Create `/var/log/crisisguardian/` directory:
```bash
sudo mkdir -p /var/log/crisisguardian
sudo chown appuser:appuser /var/log/crisisguardian
sudo chmod 755 /var/log/crisisguardian
```

### 3. Reverse Proxy (Nginx)

```nginx
upstream crisisguardian_api {
    server localhost:8000;
}

upstream crisisguardian_frontend {
    server localhost:8501;
}

server {
    listen 80;
    server_name yourdomain.com;

    location /api/ {
        proxy_pass http://crisisguardian_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://crisisguardian_frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # SSL configuration (use Let's Encrypt)
    listen 443 ssl http2;
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
}
```

### 4. Systemd Service (Linux)

```ini
# /etc/systemd/system/crisisguardian-api.service
[Unit]
Description=CrisisGuardian AI Backend API
After=network.target

[Service]
User=crisisguardian
WorkingDirectory=/opt/crisisguardian-ai
ExecStart=/opt/crisisguardian-ai/.venv/bin/python main.py
Restart=always
RestartSec=10

Environment="GEMINI_API_KEY=your_key_here"
Environment="LOG_LEVEL=INFO"

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable crisisguardian-api
sudo systemctl start crisisguardian-api
```

---

## Monitoring

### Health Checks

```bash
# API Health
curl -f http://localhost:8000/health || echo "API down"

# System Status
curl http://localhost:8000/system-status
```

### Logging

View logs in real-time:
```bash
tail -f logs/crisisguardian.log
```

---

## Security Best Practices

1. **API Keys:** Never commit `.env` files. Use secret management (AWS Secrets Manager, Azure Key Vault, etc.)
2. **HTTPS:** Always use HTTPS in production
3. **CORS:** Restrict CORS origins to your domain
4. **Rate Limiting:** Implement rate limiting (100 requests/minute per IP)
5. **Database:** Use secure database credentials
6. **Firewall:** Restrict API access to authorized IPs
7. **Logging:** Log all API access and errors

---

## Troubleshooting

### Issue: Gemini API Key not working

**Solution:** Verify key in `.env` and check API quota on Google Cloud Console.

### Issue: Port already in use

**Solution:** 
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Issue: Out of memory

**Solution:** Increase available memory or reduce batch size in processing.

---

## Rollback

To rollback to a previous version:

```bash
# With Docker
docker run --name crisisguardian-ai-v1 \
  -e GEMINI_API_KEY=your_key \
  crisisguardian-ai:v1.0.0 \
  -p 8000:8000 -p 8501:8501
```

---

## Scaling

For high-traffic scenarios:

1. **Load Balancing:** Use Nginx, HAProxy, or cloud LB
2. **API Instances:** Run multiple API instances
3. **Caching:** Implement Redis for frequently accessed data
4. **Database Optimization:** Use connection pooling
5. **Async Processing:** Use Celery for long-running tasks

---

## Support

For deployment issues, refer to:
- GitHub Issues: https://github.com/crisisguardian-ai/crisisguardian-ai/issues
- Documentation: https://crisisguardian-ai.readthedocs.io
- Email: support@crisisguardian.ai
