# Stage 1: Build the frontend
FROM node:18-alpine AS frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Build the backend
FROM python:3.9-slim AS backend
WORKDIR /app
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    python3-dev \
    make \
    gcc \
    g++ \
    pkg-config \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

# Stage 3: Combine frontend and backend
FROM python:3.9-slim
WORKDIR /app

# Copy backend
COPY --from=backend /app /app

# Copy frontend build files
COPY --from=frontend /app/build /app/frontend/build

# Expose ports (Hugging Face Spaces uses port 7860)
EXPOSE 7860

# Start the backend server
CMD ["python", "app.py"]
