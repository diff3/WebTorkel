FROM python:3.14-slim

# Basic hygiene
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Flask listens on 5000
EXPOSE 5000

# Run app
CMD ["python", "app.py"]