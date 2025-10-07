#!/bin/bash

# Check if .env file exists
if [ ! -f ../.env ] && [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with: N8N_WEBHOOK_URL=your-webhook-url"
    echo "You can copy .env.example and modify it."
    exit 1
fi

echo "🔧 Loading environment from .env file..."

# Load environment variables
if [ -f ../.env ]; then
    export $(grep -v '^#' ../.env | xargs)
elif [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Verify URL is set
if [ -z "$N8N_WEBHOOK_URL" ]; then
    echo "❌ Error: N8N_WEBHOOK_URL not found in .env file!"
    echo "Please add: N8N_WEBHOOK_URL=your-webhook-url to your .env file"
    exit 1
fi

echo "🔗 Webhook URL configured: $N8N_WEBHOOK_URL"

# Check if concurrency level is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <concurrent_requests>"
    echo "Example: $0 10"
    echo ""
    echo "This will run $1 concurrent requests against your n8n webhook"
    exit 1
fi

CONCURRENT_REQUESTS=$1

echo "🚀 Starting Go load test..."
echo "📊 Concurrent requests: $CONCURRENT_REQUESTS"
echo "🎯 Target: $N8N_WEBHOOK_URL"
echo ""

# Install dependencies if needed
if [ ! -f "go.mod" ]; then
    echo "📦 Initializing Go module..."
    go mod init webhook-loadtest
    go mod tidy
fi

# Check if godotenv package is available
if ! go list -m github.com/joho/godotenv > /dev/null 2>&1; then
    echo "📦 Installing godotenv package..."
    go get github.com/joho/godotenv
fi

# Run the load test
go run webhook_loadtest.go $CONCURRENT_REQUESTS

echo ""
echo "✅ Load test complete!"
echo "📁 Check the results directory for CSV output files"
