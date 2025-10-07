# n8n Webhook Load Tester 🚀

A comprehensive testing suite to analyze n8n webhook performance under concurrent load. Includes three different testing approaches to suit different needs and technical preferences.

## 🎯 What This Tests

This tool helps you understand n8n's concurrency limitations by systematically testing webhook endpoints with multiple concurrent requests. Perfect for:

- **SaaS builders** evaluating n8n for production workloads
- **System architects** designing high-throughput automation systems  
- **DevOps teams** planning n8n deployment strategies
- **Developers** debugging concurrency issues in n8n workflows

## 🛠️ Three Testing Methods

### 1. 🐚 Shell Tester (`01_shell_tester/`)
**Quick webhook validation**
- Simple bash script for basic testing
- Instant webhook endpoint verification  
- Perfect for quick health checks

```bash
cd 01_shell_tester
./PROD_webhook_test_external.sh
```

### 2. 🏎️ Go Load Tester (`02_go_tester/`)
**High-performance concurrent testing**
- Written in Go for maximum performance
- True concurrent HTTP requests
- Detailed CSV output with metrics
- Command-line driven with flexible parameters

```bash
cd 02_go_tester  
./run_go_load_test.sh 10  # 10 concurrent requests
```

### 3. 📊 Streamlit Web UI (`03_streamlit_tester/`)
**Interactive visual testing**
- Beautiful web interface for testing
- Real-time progress monitoring
- Visual charts and detailed results
- Perfect for demos and presentations

```bash
cd 03_streamlit_tester
streamlit run app.py
```

## ⚡ Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/cgorricho/n8n-webhook-load-tester.git
cd n8n-webhook-load-tester
```

### 2. Configure Your Webhook URL
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your n8n webhook URL
nano .env
```

Replace `[YOUR_SELF-HOSTED_N8N_URL_HERE]` with your actual webhook URL:
```
N8N_WEBHOOK_URL=https://your-domain.com/n8n/webhook/load-test
```

### 3. Install Dependencies
```bash
# For Python/Streamlit testing
pip install -r requirements.txt

# Go dependencies are auto-managed
```

### 4. Choose Your Testing Method

**Quick Test:**
```bash
cd 01_shell_tester && ./PROD_webhook_test_external.sh
```

**Load Testing:**
```bash
cd 02_go_tester && ./run_go_load_test.sh 20
```

**Interactive Testing:**
```bash
cd 03_streamlit_tester && streamlit run app.py
```

## 📊 What You'll Discover

### Typical n8n Performance Patterns
- **5 concurrent requests**: Excellent performance (~2-4s response times)
- **10 concurrent requests**: Good performance with slight delays
- **20+ concurrent requests**: Significant performance degradation
- **30+ concurrent requests**: Severe queuing and delays

### Key Metrics Measured
- **Response Times**: How long each request takes
- **Processing Overhead**: Extra time beyond workload duration
- **Success Rates**: Percentage of successful completions
- **Concurrency Patterns**: Evidence of n8n's ~5 worker limitation
- **Queueing Behavior**: How requests wait for available workers

## 🔧 Advanced Configuration

### Webhook Workflow Requirements
Your n8n workflow should:
1. Accept POST requests via webhook
2. Include a `workload_sec` parameter for simulated work
3. Return JSON with execution details
4. Generate random delays (1-5 seconds recommended)

### Example n8n Workflow Response
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

## 📈 Understanding the Results

### Go Tester CSV Output
Contains detailed metrics for analysis:
- `concurrent_requests`: Number of simultaneous requests
- `response_time_seconds`: Total request duration
- `workload_seconds`: Expected work duration
- `execution_id`: Unique n8n execution identifier
- `status`: SUCCESS/ERROR status

### Streamlit Visual Analysis
- Real-time progress tracking
- Success/failure rate monitoring
- Response time distribution charts
- Maximum concurrency achieved
- Individual execution details

## 🏗️ Repository Structure

```
n8n-webhook-load-tester/
├── 01_shell_tester/        # Basic webhook testing
│   └── PROD_webhook_test_external.sh
├── 02_go_tester/           # High-performance load testing
│   ├── webhook_loadtest.go
│   └── run_go_load_test.sh
├── 03_streamlit_tester/    # Interactive web interface
│   └── app.py
├── .env.example           # Configuration template
├── SETUP_ENV.md          # Detailed setup guide
└── requirements.txt      # Python dependencies
```

## 🔒 Security Features

- **Environment-based configuration** - No hardcoded URLs
- **Git-safe** - `.env` files automatically ignored
- **Public-ready** - Safe to share without exposing sensitive URLs
- **Template-driven** - Easy setup with `.env.example`

## 🎯 Use Cases

### For SaaS Builders
- Validate n8n can handle your expected user load
- Plan architecture around n8n's concurrency limits
- Make data-driven decisions about automation scaling

### For System Architects  
- Understand n8n's Task Runner architecture limitations
- Design hybrid systems that work around constraints
- Plan horizontal scaling strategies

### For DevOps Teams
- Benchmark different n8n deployment configurations
- Test performance across development/staging/production
- Monitor automation system health and capacity

## 📚 Additional Resources

- `SETUP_ENV.md` - Detailed environment configuration guide
- `results/` - Generated test output files (CSV, logs)
- Individual tool README files in each testing directory

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the testing suite!

## 📄 License

MIT License - Use this tool to test and understand n8n's capabilities for your projects.

---

**Ready to discover n8n's concurrency limits?** Start with the shell test, then use the Go tester for serious load analysis, and the Streamlit app for visual exploration! 🚀
