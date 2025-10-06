# n8n Webhook Load Tester - Go Edition 🚀

A high-performance, concurrent load tester written in Go for testing n8n webhook endpoints.

## Features

- ⚡ **True Concurrency**: Uses Go routines for genuine concurrent HTTP requests
- 📊 **Detailed Statistics**: Response times, success rates, throughput analysis
- 🎯 **Precise Timing**: Microsecond-level timing precision
- 🔍 **Comprehensive Reporting**: Individual request results with execution IDs
- 🐳 **Docker Fallback**: Automatically uses Docker if Go is not installed
- 🛡️ **Error Handling**: Robust error detection and reporting

## Installation

No installation required! The script automatically:
1. Uses local Go installation if available
2. Falls back to official Docker golang image if Go is not installed

## Usage

### Basic Usage
```bash
./run_go_load_test.sh <number_of_requests>
```

### Examples
```bash
# Light load test
./run_go_load_test.sh 10

# Medium load test  
./run_go_load_test.sh 50

# Heavy load test
./run_go_load_test.sh 100

# Stress test
./run_go_load_test.sh 500
```

## Sample Output

```
🚀 Starting n8n Webhook Load Test
📊 Configuration:
   - Target URL: https://carlosgorrichoai.one/n8n/webhook/load-test
   - Total Requests: 3
   - Concurrency: All requests launched simultaneously

⏱️  Test started at: 2025-10-06 00:42:34

📈 LOAD TEST RESULTS
==========================================

📊 Overall Statistics:
   Total Requests:     3
   Successful:         3 (100.0%)
   Failed:             0 (0.0%)
   Total Duration:     7.5810891s
   Requests/Second:    0.40

⏱️  Response Time Statistics:
   Average:            6.526874481s
   Minimum:            5.131653854s
   Maximum:            7.579650306s

📋 Detailed Request Results:
ID  | Status | Time    | Execution ID                    | Delay | Description
----+--------+---------+---------------------------------+-------+------------------
1   | ✅ OK   |    5.1s | exec-1759725758971-m32l871d3    | 1s    | Simulated 1s...
2   | ✅ OK   |    7.6s | exec-1759725758417-5f4717b30    | 4s    | Simulated 4s...
3   | ✅ OK   |    6.9s | exec-1759725758707-vfz7wa0q4    | 3s    | Simulated 3s...

🎯 Test completed successfully!
```

## Files

- `webhook_loadtest.go` - Main Go load tester program  
- `run_go_load_test.sh` - Shell script wrapper with Docker fallback
- `GO_LOAD_TESTER_README.md` - This documentation

## Comparison with Streamlit App

| Feature | Go Load Tester | Streamlit App |
|---------|----------------|---------------|
| **Concurrency** | True Go routines | Python asyncio |
| **Performance** | ⚡ Highest | 🔄 Good |  
| **Interface** | 📟 CLI/Terminal | 🖥️ Web UI |
| **Real-time Updates** | ❌ Final results only | ✅ Live progress |
| **Detailed Stats** | ✅ Comprehensive | ✅ Good |
| **Portability** | 🐳 Docker fallback | 🐍 Python required |
| **Output Format** | 📊 Formatted tables | 📈 Interactive UI |

## Use Cases

- **Performance Benchmarking**: Measure n8n webhook throughput
- **Concurrency Testing**: Test how many simultaneous requests n8n can handle  
- **Response Time Analysis**: Analyze latency patterns
- **Stress Testing**: Push n8n to its limits
- **CI/CD Integration**: Automated performance regression testing

## Configuration

The webhook URL is hardcoded in `webhook_loadtest.go`:
```go
const webhookURL = "https://carlosgorrichoai.one/n8n/webhook/load-test"
```

To change the target URL, edit this constant and rerun the script.

## Requirements

- **Option 1**: Go 1.13+ (automatically detected)
- **Option 2**: Docker (automatic fallback)
- **Target**: Active n8n webhook endpoint

## Troubleshooting

### "Go not found" 
✅ **Solution**: Script automatically uses Docker - no action needed

### "Docker not available"
❌ **Problem**: Neither Go nor Docker is installed  
✅ **Solution**: Install either Go or Docker

### "Compilation failed"
❌ **Problem**: Go compilation error  
✅ **Solution**: Check Go version, try Docker mode

---

🎯 **Ready to stress-test your n8n webhooks with Go-powered concurrency!**
