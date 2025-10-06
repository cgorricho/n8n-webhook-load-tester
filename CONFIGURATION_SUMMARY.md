# n8n Webhook Load Tester - Final Configuration

## ✅ WORKING CONFIGURATION

### Webhook URLs:
- **Streamlit App**: `https://carlosgorrichoai.one/n8n/webhook/load-test`
- **External Test Script**: `https://carlosgorrichoai.one/n8n/webhook/load-test`
- **Localhost Test Script**: `http://localhost:5678/webhook/load-test`

### n8n Workflow:
- **Name**: "Webhook Load Test - Random Workload"
- **Status**: Active
- **Webhook Path**: `"webhook/load-test"`
- **Method**: POST
- **Response Mode**: responseNode

### Expected Response Format:
```json
{
  "message": "work complete",
  "executionId": "exec-1759725454831-hz6rn6du1",
  "delaySeconds": 4,
  "startTime": "2025-10-06T04:37:34.831Z",
  "endTime": "2025-10-06T04:37:38.832Z",
  "workloadDescription": "Simulated 4s workload"
}
```

### Usage:
1. **Single Test**: Run `./PROD_webhook_test_external.sh`
2. **Load Testing**: Run `streamlit run app.py`

### Status: ✅ READY FOR USE
