# 🎯 Complete Setup Summary

## ✅ What's Ready to Use

### n8n Workflow
- **Workflow Name**: Webhook Load Test - Random Workload
- **Webhook URL**: `https://carlosgorrichoai.one/n8n/webhook-test/load-test`
- **Features**:
  - ✅ Unique execution ID per run
  - ✅ Random 1-5 second workload simulation
  - ✅ Complete response with timing details
  - ⚠️ **Action Required**: Activate the workflow in n8n

### Streamlit App
- **Repository**: https://github.com/cgorricho/n8n-webhook-load-tester
- **Pre-configured with**: Your webhook URL hardcoded
- **Features**:
  - ✅ Async concurrent requests
  - ✅ Real-time concurrency monitoring
  - ✅ Detailed execution tracking
  - ✅ Clean, minimal interface

## 🚀 Quick Start (3 Commands)

```bash
git clone https://github.com/cgorricho/n8n-webhook-load-tester.git
cd n8n-webhook-load-tester
pip install -r requirements.txt
streamlit run app.py
```

Then:
1. Activate the n8n workflow
2. Click "Start Load Test" in the app
3. Watch concurrent executions in real-time!

## 📊 Sample Response

When the workflow runs, it returns:
```json
{
  "message": "work complete",
  "executionId": "exec-1728095087123-x9k2m7p4q",
  "delaySeconds": 3,
  "startTime": "2025-10-05T02:34:52.287Z",
  "endTime": "2025-10-05T02:34:55.287Z",
  "workloadDescription": "Simulated 3s workload"
}
```

## 🔍 What You'll See

**App Dashboard:**
- 🔄 Currently Running - Live count of active requests
- 📈 Max Concurrent - Peak simultaneous executions
- ✅ Success/❌ Failure counts
- ⏱️ Average response time
- ⏰ Total test duration

**Results Table:**
- Request ID
- Status (✅/❌)
- **Execution ID** (unique per workflow run)
- Message
- Workload description
- Response time

## 🎯 Testing Your Concurrency

**Start small:**
- Begin with 10 requests
- Watch the "Currently Running" counter
- Note the "Max Concurrent" value

**Scale up:**
- Try 20, 30, 50 requests
- Compare max concurrent executions
- Identify queuing behavior (if any)

## 📝 Files in Repository

```
n8n-webhook-load-tester/
├── app.py                    # Main Streamlit app (webhook URL hardcoded)
├── requirements.txt          # Python dependencies
├── README.md                 # Full documentation
├── SETUP.md                  # Quick setup guide
├── EXAMPLE_RESPONSE.md       # Response format details
├── test_webhook.sh          # Manual curl test script
└── .streamlit/
    └── config.toml          # Streamlit configuration
```

## 🔧 No Configuration Needed!

Since your n8n server is protected with API keys and 2FA:
- ✅ Webhook URL is hardcoded in the app
- ✅ No environment variables needed
- ✅ No API keys to configure
- ✅ Just clone and run!

## 💡 Use Cases

1. **Find concurrency limits** - See how many workflows run simultaneously
2. **Performance testing** - Measure response times under load
3. **Queue behavior** - Observe if/when n8n queues executions
4. **Debugging** - Track individual executions with unique IDs
5. **Benchmarking** - Compare different instance configurations

## 🎉 You're All Set!

Just activate your workflow and run the app. Everything else is ready to go!
