# MadadgaarAI Production Deployment & Hosting Guide

This guide details best practices for deploying MadadgaarAI in production environments, including Linux server setup, reverse proxy configuration with Nginx, process supervision with Systemd, and Docker containerization.

---

## 1. System Requirements

- **Operating System**: Ubuntu 22.04 LTS / Debian 12 / Windows Server 2022
- **CPU**: 2+ vCPU cores (4+ vCPU recommended for real-time dense vector inference)
- **RAM**: 4 GB minimum (8 GB recommended for caching PyTorch & SentenceTransformers)
- **Disk**: 10 GB SSD storage
- **Python**: 3.10, 3.11, or 3.12

---

## 2. Linux Production Deployment (Systemd + Uvicorn)

### 2.1 Set Up System User & Repository
```bash
sudo useradd -m -s /bin/bash madadgaar
sudo -u madadgaar git clone https://github.com/3tbhai/MadadgarAI.git /opt/madadgaar
cd /opt/madadgaar
sudo -u madadgaar python3 -m venv venv
sudo -u madadgaar ./venv/bin/pip install --upgrade pip
sudo -u madadgaar ./venv/bin/pip install -r requirements.txt
```

### 2.2 Systemd Service Unit (`/etc/systemd/system/madadgaar.service`)
```ini
[Unit]
Description=MadadgaarAI National Scholarship & Funding Engine
After=network.target

[Service]
User=madadgaar
Group=madadgaar
WorkingDirectory=/opt/madadgaar
Environment="PATH=/opt/madadgaar/venv/bin"
Environment="MADADGAAR_HOST=127.0.0.1"
Environment="MADADGAAR_PORT=8000"
Environment="HF_HUB_OFFLINE=1"
ExecStart=/opt/madadgaar/venv/bin/python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now madadgaar
sudo systemctl status madadgaar
```

---

## 3. Nginx Reverse Proxy & SSL (Let's Encrypt)

```nginx
server {
    listen 80;
    server_name funding.madadgaar.gov.in;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_read_timeout 120s;
    }
}
```

---

## 4. Docker Containerization

### Dockerfile
```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HUB_ENABLE_HF_TRANSFER=0

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tesseract-ocr \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Warm up model cache
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
