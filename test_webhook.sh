#!/bin/bash

# Test the n8n webhook manually - PRODUCTION endpoint

WEBHOOK_URL="https://carlosgorrichoai.one/n8n/webhook/load-test"

echo "Testing PRODUCTION webhook: $WEBHOOK_URL"
echo ""

# Single test request
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"request_id": 1, "test": true}' \
  | jq .

echo ""
echo "If you see a 'work complete' message with an executionId, the webhook is working!"
echo ""
echo "If you get a 404 error about 'webhook not registered', the production webhook"
echo "may not be publicly accessible. Check your n8n logs and reverse proxy config."
echo ""
echo "To test multiple concurrent requests, use the Streamlit app:"
echo "  streamlit run app.py"
