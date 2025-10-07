# Environment Setup

## 🔧 Initial Configuration

Before running any tests, you need to configure your n8n webhook URL:

### 1. Copy the example environment file:
```bash
cp .env.example .env
```

### 2. Edit the .env file and replace the placeholder:
```bash
# Open .env in your editor
nano .env

# Replace this:
N8N_WEBHOOK_URL=[YOUR_SELF-HOSTED_N8N_URL_HERE]

# With your actual webhook URL, for example:
N8N_WEBHOOK_URL=https://your-domain.com/n8n/webhook/load-test
```

### 3. Common URL formats:
```bash
# Self-hosted with domain:
N8N_WEBHOOK_URL=https://n8n.yourcompany.com/webhook/load-test

# Local development:
N8N_WEBHOOK_URL=http://localhost:5678/webhook/load-test

# Custom webhook path:
N8N_WEBHOOK_URL=https://your-domain.com/n8n/webhook/your-workflow-name
```

## 🔒 Security Note

The `.env` file is automatically ignored by Git and will not be pushed to repositories. This keeps your webhook URLs and any other sensitive configuration private.

## ✅ Verification

All three testing methods will automatically:
1. Load the URL from your `.env` file
2. Display the configured URL before testing
3. Show clear error messages if configuration is missing

## 🚀 Ready to Test

Once configured, you can run any of the testing methods:

- **Shell Test**: `cd 01_shell_tester && ./PROD_webhook_test_external.sh`
- **Go Load Test**: `cd 02_go_tester && ./run_go_load_test.sh    # Defaults to 10 requests`
- **Streamlit UI**: `cd 03_streamlit_tester && streamlit run app.py`

All will use the same URL configuration from your `.env` file!
