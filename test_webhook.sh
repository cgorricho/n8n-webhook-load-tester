#!/bin/bash

# Test the n8n webhook manually
# URL is hardcoded in the app

WEBHOOK_URL="https://carlosgorrichoai.one/n8n/webhook-test/load-test"

echo "Testing webhook: $WEBHOOK_URL"
echo ""

# Single test request
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"request_id": 1, "test": true}' \
  | jq .

echo ""
echo "If you see a 'work complete' message with an executionId, the webhook is working!"
echo ""
echo "To test multiple concurrent requests, use the Streamlit app:"
echo "  streamlit run app.py"
