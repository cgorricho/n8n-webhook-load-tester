#!/bin/bash

# Test the n8n webhook manually - Uses environment variable from .env file

# Load environment variables from .env file
if [ -f ../.env ]; then
    export $(grep -v '^#' ../.env | xargs)
elif [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with: N8N_WEBHOOK_URL=your-webhook-url"
    echo "You can copy .env.example and modify it."
    exit 1
fi

# Check if webhook URL is set
if [ -z "$N8N_WEBHOOK_URL" ]; then
    echo "❌ Error: N8N_WEBHOOK_URL not found in .env file!"
    echo "Please add: N8N_WEBHOOK_URL=your-webhook-url to your .env file"
    exit 1
fi

echo "🔗 Using webhook URL: $N8N_WEBHOOK_URL"
echo "🧪 Testing webhook endpoint..."

# Make the test request
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Shell script test",
    "workload_sec": 2,
    "timestamp": "'$(date -Iseconds)'"
  }' \
  "$N8N_WEBHOOK_URL"

echo ""
echo "✅ Test complete!"
echo "If you see a 'work complete' message with an executionId, the webhook is working!"
