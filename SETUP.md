# Quick Setup Guide

## ✅ What's Been Created

### 1. n8n Workflow
- **Name**: "Webhook Load Test - Random Workload"
- **ID**: `9Eo6dcyKwmLpWDw8`
- **Webhook Path**: `/load-test`
- **Status**: ⚠️ Currently INACTIVE - needs to be activated

### 2. GitHub Repository
- **URL**: https://github.com/cgorricho/n8n-webhook-load-tester
- **Contains**:
  - `app.py` - Streamlit application with async webhook caller
  - `requirements.txt` - Python dependencies
  - `README.md` - Full documentation
  - `.streamlit/config.toml` - App configuration

## 🚀 Next Steps

### Step 1: Activate the n8n Workflow

**IMPORTANT**: The workflow is currently inactive. You need to activate it:

1. Go to your n8n instance
2. Open the workflow "Webhook Load Test - Random Workload"
3. Click the **Activate** toggle in the top right
4. Copy the webhook URL (it will be shown when active)

The webhook URL will be in this format:
```
https://your-n8n-instance.com/webhook/load-test
```

Or for production webhooks:
```
https://your-n8n-instance.com/webhook-test/load-test
```

### Step 2: Run the Streamlit App

```bash
# Clone the repo
git clone https://github.com/cgorricho/n8n-webhook-load-tester.git
cd n8n-webhook-load-tester

# Install dependencies
pip install -r requirements.txt

# (Optional) Set webhook URL as environment variable
export N8N_WEBHOOK_URL="https://your-n8n-instance.com/webhook/load-test"

# Run the app
streamlit run app.py
```

### Step 3: Test Concurrency

1. Open the app in your browser (usually http://localhost:8501)
2. Enter your webhook URL in the sidebar
3. Set number of requests (start with 10)
4. Click "Start Load Test"
5. Watch the concurrent execution counter in real-time!

## 📊 What to Expect

- **Single workflow, multiple executions**: The app will call the same webhook URL multiple times
- **Random workload**: Each execution will take 1-5 seconds (random)
- **Concurrent tracking**: You'll see how many requests are running simultaneously
- **n8n behavior**:
  - **Cloud**: May queue requests if you hit concurrency limits
  - **Self-hosted**: Will run all requests concurrently (unless limits configured)

## 🔧 Workflow Details

The n8n workflow does:

1. **Webhook Trigger** - Accepts POST requests at `/load-test`
2. **Random Delay** - Simulates work with 1-5 second random delay
3. **Response** - Returns JSON with:
   ```json
   {
     "message": "work complete",
     "delaySeconds": 3,
     "startTime": "2025-10-05T02:34:52.123Z",
     "endTime": "2025-10-05T02:34:55.123Z",
     "workloadDescription": "Simulated 3s workload"
   }
   ```

## 💡 Tips

- Start with **5-10 requests** to see how your instance handles concurrency
- Watch the **"Currently Running"** metric - this shows true concurrency
- **Max Concurrent** tells you the peak simultaneous executions
- If you see queuing behavior, you've hit your concurrency limit
- Check n8n executions tab to see all the workflow runs

## 🐛 Troubleshooting

**"Please configure a valid webhook URL"**
- Make sure you've activated the n8n workflow
- Copy the exact webhook URL from n8n
- Include the full URL with https://

**All requests fail**
- Verify the workflow is active (green toggle in n8n)
- Check if your n8n instance is accessible from your machine
- Try the webhook URL in Postman/curl first

**No concurrent executions**
- This is normal if requests complete very quickly
- Try increasing the number of requests
- The random delay ensures some overlap

## 📚 Learn More

See the full README.md for detailed information about metrics, use cases, and how everything works.
