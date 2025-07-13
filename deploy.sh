#!/bin/bash

# Trip Cost Calculator Deployment Script
# Usage: ./deploy.sh [registry-url] [image-tag]

set -e

# Default values
REGISTRY_URL=${1:-"your-mikrus-registry"}
IMAGE_TAG=${2:-"latest"}
IMAGE_NAME="trip-calculator-api"

echo "🚀 Starting deployment process..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your API keys:"
    echo "API_KEY=your_google_maps_api_key"
    echo "WEATHER_API=your_openweathermap_api_key"
    exit 1
fi

# Build Docker image
echo "📦 Building Docker image..."
docker build -t $IMAGE_NAME:$IMAGE_TAG .

# Tag for registry
echo "🏷️  Tagging image for registry..."
docker tag $IMAGE_NAME:$IMAGE_TAG $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG

# Push to registry
echo "⬆️  Pushing to registry..."
docker push $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG

echo "✅ Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Go to your mikr.us dashboard"
echo "2. Create a new container with image: $REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG"
echo "3. Configure environment variables from your .env file"
echo "4. Expose port 5001"
echo "5. Enable SSL certificate"
echo ""
echo "🔗 Your backend will be available at: https://your-mikrus-domain.com"
echo "📝 Don't forget to update NEXT_PUBLIC_API_URL in your Vercel deployment!" 