# Quick Setup Guide

## ✅ What's Been Created

### 1. n8n Workflow
- **Name**: "Webhook Load Test - Random Workload"
- **ID**: `9Eo6dcyKwmLpWDw8`
- **Webhook URL**: `https://carlosgorrichoai.one/n8n/webhook-test/load-test`
- **Status**: ⚠️ Make sure it's ACTIVATED in n8n

### 2. GitHub Repository
- **URL**: https://github.com/cgorricho/n8n-webhook-load-tester
- **Contains**:
  - `app.py` - Streamlit application with async webhook caller (webhook URL pre-configured)
  - `requirements.txt` - Python dependencies
  - `README.md` - Full documentation

## 🚀 Quick Start (3 Steps)

### Step 1: Activate the n8n Workflow

1. Go to your n8n instance at `https://carlosgorrichoai.one/n8n`
2. Open the workflow "Webhook Load Test - Random Workload"
3. Click the **Activate** toggle in the top right (must be green/ON)

### Step 2: Clone and Install

```bash
# Clone the repo
git clone https://github.com/cgorricho/n8n-webhook-load-tester.git
cd n8n-webhook-load-tester

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Run the App

```bash
streamlit run app.py
```

That's it! The app will open in your browser at http://localhost:8501

## 📊 Using the Load Tester

1. Use the slider to set how many concurrent requests (default: 10)
2. Click "🚀 Start Load Test"
3. Watch the real-time metrics:
   - **Currently Running** - Active webhook calls right now
   - **Max Concurrent** - Peak simultaneous executions
4. Review detailed results including unique execution IDs

## 🔧 Configuration

The webhook URL is **hardcoded** in the app:
```
https://carlosgorrichoai.one/n8n/webhook-test/load-test
```

No environment variables needed! Your n8n server is protected by API key and 2FA, so the webhook is publicly accessible for testing.

## 📋 What to Expect

- **Each execution takes 1-5 seconds** (random)
- **All requests launch simultaneously** (true async concurrency)
- **Unique execution ID** for each workflow run (e.g., `exec-1728095087123-abc123def`)
- **Response includes**:
  - Message: "work complete"
  - Execution ID
  - Delay duration
  - Start/end timestamps
  - Workload description

## 🐛 Troubleshooting

**All requests fail:**
- Make sure the n8n workflow is **activated** (green toggle)
- Verify you can access `https://carlosgorrichoai.one/n8n`

**No concurrent executions shown:**
- This is normal if requests complete very quickly
- Try increasing the number of requests (e.g., 20-30)
- The random 1-5 second delay ensures some overlap

**Want to test the webhook manually?**
```bash
curl -X POST "https://carlosgorrichoai.one/n8n/webhook-test/load-test" \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

You should get back a JSON response with "work complete" and a unique execution ID.

## 📚 Next Steps

- Start with 10 requests to see baseline performance
- Gradually increase to find your concurrency sweet spot
- Check n8n's executions tab to see all the workflow runs
- Each execution will have its unique ID matching the app's results

Ready to test? Just run `streamlit run app.py` and click the button! 🚀
