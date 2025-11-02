# Sử dụng image Python nhẹ
FROM python:3.13-slim

# Đặt biến môi trường để tránh tạo file .pyc và đảm bảo stdout/stderr được ghi ngay lập tức
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expose cổng chạy FastAPI (mặc định 8000)
EXPOSE 8000

# Chạy ứng dụng với uvicorn
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
