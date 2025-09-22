# 使用一个官方的Python基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装Tesseract OCR引擎及其语言包
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# 将requirements.txt复制到工作目录
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 将所有本地代码复制到容器中
COPY . .

# 定义启动命令
CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:$PORT", "app:app"]