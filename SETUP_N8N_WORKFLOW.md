# n8n Workflow Setup Guide 📋

This guide explains how to set up the required n8n workflow for load testing.

## 🎯 What This Workflow Does

The `n8n_load_test_workflow.json` contains a simple but effective workflow that:

1. **Receives webhook requests** on `/webhook/load-test` endpoint
2. **Generates unique execution IDs** for tracking individual requests
3. **Simulates random workload** (1-5 seconds of processing time)
4. **Returns detailed JSON response** with timing and execution data

This design allows you to test how n8n handles concurrent requests with realistic processing delays.

## 🚀 Quick Setup

### 1. Import the Workflow
```
1. Open your n8n interface
2. Click "+" to create a new workflow
3. Click the "..." menu → "Import from file"
4. Select the `n8n_load_test_workflow.json` file
5. Click "Save" to save the imported workflow
```

### 2. Activate the Workflow
```
⚠️ CRITICAL: The workflow MUST be activated to receive webhook calls!

1. Click the "Active/Inactive" toggle in the top-right corner
2. Ensure it shows "Active" (green)
3. The webhook is now ready to receive requests
```

### 3. Get Your Webhook URL
```
1. Click on the "Webhook" node in your workflow
2. Copy the "Production URL" shown in the node sidebar
3. It will look like: https://your-domain.com/n8n/webhook/load-test
4. Use this URL in your .env configuration
```

## 🔧 Workflow Components

### Node 1: Webhook Trigger
- **Type**: `n8n-nodes-base.webhook`
- **Method**: POST
- **Path**: `load-test`
- **Response Mode**: `responseNode` (waits for workflow completion)

### Node 2: Random Delay (Code)
- **Type**: `n8n-nodes-base.code`
- **Purpose**: Simulates realistic processing workload
- **Logic**: 
  - Generates unique execution ID
  - Creates random delay (1-5 seconds)
  - Records start/end timestamps
  - Simulates actual work processing

### Node 3: Respond to Webhook
- **Type**: `n8n-nodes-base.respondToWebhook`
- **Format**: JSON response
- **Content**: Passes through all data from the Code node

## 📊 Expected Response Format

When working correctly, the webhook returns:

```json
{
  "message": "work complete",
  "executionId": "exec-1759860348863-xq4u59tmm",
  "delaySeconds": 3,
  "startTime": "2025-10-07T18:05:48.864Z",
  "endTime": "2025-10-07T18:05:51.866Z",
  "workloadDescription": "Simulated 3s workload"
}
```

## ⚠️ Critical Setup Requirements

### 1. Workflow MUST Be Active
```
❌ COMMON MISTAKE: Importing but not activating the workflow
✅ SOLUTION: Always check the "Active" toggle is ON (green)

If the workflow is inactive:
- Webhook calls will return 404 errors
- No executions will be recorded
- Load tests will fail completely
```

### 2. Webhook URL Configuration
```
The webhook URL format is:
https://your-n8n-domain.com/n8n/webhook/{path}

Where {path} matches the "path" parameter in the Webhook node.
Our workflow uses path: "load-test"
```

### 3. Response Mode Settings
```
The Webhook node MUST use "responseMode": "responseNode"
This ensures the webhook waits for the entire workflow to complete
before returning a response to the load tester.
```

## 🧪 Testing Your Setup

### Quick Verification
```bash
# Test with curl (replace with your webhook URL)
curl -X POST https://your-domain.com/n8n/webhook/load-test \
  -H "Content-Type: application/json" \
  -d '{"test": "verification"}'

# Expected: JSON response with executionId and timing data
```

### Using the Load Testers
```bash
# Shell test (quickest verification)
cd 01_shell_tester
./PROD_webhook_test_external.sh

# Go load test (3 concurrent requests)
cd 02_go_tester  
./run_go_load_test.sh     # Defaults to 10 requests
./run_go_load_test.sh 3   # Or specify custom amount

# Streamlit interface (visual testing)
cd 03_streamlit_tester
streamlit run app.py
```

## 🔍 Troubleshooting

### Problem: 404 Not Found
**Cause**: Workflow is not active or webhook path is incorrect
**Solution**: 
1. Activate the workflow in n8n
2. Verify webhook path matches your URL
3. Check your n8n instance is running

### Problem: No Response/Timeout
**Cause**: Response mode not configured correctly
**Solution**:
1. Check Webhook node has "responseMode": "responseNode"
2. Ensure "Respond to Webhook" node is connected
3. Verify workflow execution completes successfully

### Problem: Invalid JSON Response
**Cause**: Code node error or connection issues
**Solution**:
1. Test the workflow manually in n8n
2. Check Code node for JavaScript errors
3. Verify all nodes are properly connected

## 🎛️ Customization Options

### Adjust Workload Range
Edit the Code node to change delay range:
```javascript
// Current: 1-5 seconds
const delaySeconds = Math.floor(Math.random() * 5) + 1;

// Example: 2-10 seconds  
const delaySeconds = Math.floor(Math.random() * 9) + 2;
```

### Add Request Processing
You can extend the Code node to:
- Process request body data
- Add database operations
- Include external API calls
- Log execution details

### Change Webhook Path
Modify the Webhook node "path" parameter:
- Current: `/webhook/load-test`
- Custom: `/webhook/your-custom-path`
- Update your .env file accordingly

## 📈 Performance Notes

### n8n Behavior Under Load
- **1-5 concurrent**: Excellent performance
- **10+ concurrent**: Starts queuing requests  
- **20+ concurrent**: Significant delays due to ~5 worker limit
- **30+ concurrent**: Heavy queuing, potential timeouts

### Why This Design Works
1. **Realistic workload**: Random delays simulate real processing
2. **Unique tracking**: Each execution gets a unique ID
3. **Timing data**: Start/end timestamps show actual processing time
4. **JSON response**: Structured data for analysis

## ✅ Verification Checklist

Before starting load tests, verify:

- [ ] Workflow imported successfully
- [ ] Workflow is **ACTIVE** (green toggle)
- [ ] Webhook node shows production URL
- [ ] Manual test returns expected JSON
- [ ] .env file has correct webhook URL
- [ ] All testing tools can reach the endpoint

Your n8n workflow is now ready for comprehensive concurrency testing! 🚀
