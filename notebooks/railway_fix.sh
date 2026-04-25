#!/bin/bash

echo "=== 修复 Railway 部署（精简版） ==="

# 1. 备份原文件
cp requirements.txt requirements.txt.backup 2>/dev/null
cp server.py server.py.backup 2>/dev/null

# 2. 创建精简 requirements.txt
cat > requirements.txt << 'REQ'
fastapi==0.136.1
uvicorn[standard]==0.46.0
python-multipart==0.0.26
opencv-python-headless==4.13.0.92
ultralytics==8.4.41
pillow==12.2.0
numpy==2.2.5
REQ

echo "✅ 精简版 requirements.txt 已创建"

# 3. 更新 server.py（移除 torch 依赖）
sed -i 's/import cv2/from PIL import Image\nimport numpy as np/' server.py 2>/dev/null

echo "✅ server.py 已更新"

# 4. 创建配置文件
cat > Procfile << 'EOF'
web: uvicorn server:app --host 0.0.0.0 --port $PORT
