# n8n Webhook Load Tester 🚀

A simple Streamlit app to test concurrent webhook executions on your n8n workflows.

## Features

- 🔄 **Async requests** - Uses Python asyncio and aiohttp for true concurrent execution
- 📊 **Real-time monitoring** - Watch concurrent executions in real-time
- 📈 **Detailed metrics** - Success/failure rates, timing, and workload info
- 🆔 **Unique execution tracking** - Each workflow execution has a unique timestamp-based ID
- ⚙️ **Configurable** - Adjust number of concurrent requests via slider

## Setup

### Prerequisites

1. **n8n workflow** - You need an active n8n workflow with a webhook trigger
   - The workflow should be created with the webhook path `/load-test`
   - It includes a random 1-5 second delay to simulate workload
   - Returns a "work complete" message with timing info and unique execution ID

2. **Python 3.8+** installed

### Installation

```bash
# Clone the repository
git clone https://github.com/cgorricho/n8n-webhook-load-tester.git
cd n8n-webhook-load-tester

# Install dependencies
pip install -r requirements.txt
```

### Configuration

You can set your webhook URL in two ways:

1. **Environment variable** (recommended):
```bash
export N8N_WEBHOOK_URL="https://your-n8n-instance.com/webhook/load-test"
```

2. **In the app** - Enter it in the sidebar when running

## Usage

### Run the Streamlit app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the app

1. **Enter your webhook URL** in the sidebar (or set via environment variable)
2. **Set the number of requests** using the slider (1-50)
3. **Click "Start Load Test"** to begin
4. **Monitor** the concurrent executions in real-time
5. **Review results** including success rate, timing, execution IDs, and individual request details

## How it works

### The n8n Workflow

The test workflow:
1. Receives a POST request via webhook
2. Generates a unique execution ID based on timestamp (e.g., `exec-1728095087123-abc123def`)
3. Generates a random delay between 1-5 seconds
4. Waits for that duration (simulating work)
5. Returns a JSON response with:
   - `message`: "work complete"
   - `executionId`: Unique identifier for this specific execution
   - `delaySeconds`: The random delay used
   - `startTime` and `endTime`: ISO timestamps
   - `workloadDescription`: Human-readable description

### The Streamlit App

The app:
1. Creates async HTTP requests using `aiohttp`
2. Launches all requests concurrently
3. Tracks how many are running at any given time
4. Records the maximum concurrent executions
5. Displays detailed results for each request including unique execution IDs

## Metrics Explained

- **Currently Running**: Number of webhook calls executing right now
- **Max Concurrent**: Highest number of simultaneous executions during the test
- **Successful**: Requests that completed successfully
- **Failed**: Requests that encountered errors
- **Avg Time**: Average response time across all requests
- **Total Time**: Total elapsed time for the entire test
- **Execution ID**: Unique identifier for each workflow execution (visible in results table)

## Use Cases

- Test your n8n instance's concurrency limits
- Validate webhook performance under load
- Understand how n8n queues executions
- Compare Cloud vs self-hosted concurrency behavior
- Debug race conditions in workflows
- Track individual workflow executions with unique IDs

## License

MIT
