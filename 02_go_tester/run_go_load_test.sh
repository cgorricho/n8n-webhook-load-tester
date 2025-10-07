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

# Set concurrent requests (default to 10 if not provided)
if [ $# -eq 0 ]; then
    CONCURRENT_REQUESTS=10
    echo "🎯 Using default: 10 concurrent requests"
    echo "💡 Tip: You can specify a different number: $0 <concurrent_requests>"
else
    CONCURRENT_REQUESTS=$1
fi

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
echo "📁 Check the 02_go_tester/results directory for CSV output files"
