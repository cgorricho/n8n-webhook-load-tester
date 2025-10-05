#!/bin/bash

# Test the n8n webhook manually
# Replace with your actual webhook URL

WEBHOOK_URL="${N8N_WEBHOOK_URL:-https://your-n8n-instance.com/webhook/load-test}"

echo "Testing webhook: $WEBHOOK_URL"
echo ""

# Single test request
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"request_id": 1, "test": true}' \
  | jq .

echo ""
echo "If you see a 'work complete' message, the webhook is working!"
echo ""
echo "To test multiple concurrent requests, use the Streamlit app:"
echo "  streamlit run app.py"
