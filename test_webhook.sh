#!/bin/bash

# Test the n8n webhook manually - PRODUCTION endpoint (localhost)

WEBHOOK_URL="https://carlosgorrichoai.one/n8n/webhook/load-test"

echo "Testing PRODUCTION webhook: $WEBHOOK_URL"
echo ""

# Single test request - no jq to see raw response
echo "Raw response:"
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"request_id": 1, "test": true}'

echo ""
echo ""
echo "If you see a 'work complete' message with an executionId, the webhook is working!"
echo ""
echo "To test multiple concurrent requests, use the Streamlit app:"
echo "  streamlit run app.py"
