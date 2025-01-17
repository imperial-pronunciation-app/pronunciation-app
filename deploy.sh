#!/bin/bash

set -e  # Exit on any error

# Required environment variables
: "${DOCKERHUB_USERNAME:?Must set DOCKERHUB_USERNAME}"
: "${DOCKERHUB_ACCESS_TOKEN:?Must set DOCKERHUB_ACCESS_TOKEN}"
: "${IMAGE_NAME:?Must set IMAGE_NAME}"
: "${IMAGE_TAG:?Must set IMAGE_TAG}"

# Optional configuration with defaults
CONTAINER_NAME=${CONTAINER_NAME:-"flask-api"}
CONTAINER_PORT=${CONTAINER_PORT:-443}
HOST_PORT=${HOST_PORT:-443}

echo "🔑 Logging into Docker Hub..."
echo "$DOCKERHUB_ACCESS_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

echo "⬇️ Pulling image ${IMAGE_NAME}:${IMAGE_TAG}..."
docker pull "${IMAGE_NAME}:${IMAGE_TAG}"

echo "🛑 Stopping existing container..."
docker stop "$CONTAINER_NAME" || true
docker rm "$CONTAINER_NAME" || true

echo "🚀 Starting new container..."
docker run -d \
  --name "$CONTAINER_NAME" \
  --restart unless-stopped \
  -p "${HOST_PORT}:${CONTAINER_PORT}" \
  "${IMAGE_NAME}:${IMAGE_TAG}"

echo "🧹 Cleaning up old images..."
docker system prune -f

echo "✅ Deployment complete!"