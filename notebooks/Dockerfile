FROM python:3.11-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有代码
COPY . .

# 使用环境变量 PORT（Railway 自动注入）
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port $PORT"]
