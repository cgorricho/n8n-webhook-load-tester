# n8n Webhook Load Tester

Comprehensive concurrency testing suite that systematically analyzes n8n webhook performance under load. Built for SaaS builders, system architects, and DevOps teams evaluating n8n for production workloads.

## Why This Exists

n8n is powerful for workflow automation, but its concurrency behavior under load is poorly documented. If you're building a SaaS product on n8n, you need to know: How many concurrent webhook requests can it handle? What happens when you exceed that limit? Where's the breaking point?

This tool answers those questions with data.

## What It Tests

The load tester sends configurable bursts of concurrent requests to an n8n webhook endpoint, measuring:

- **Throughput** — requests processed per second
- **Concurrency handling** — how many simultaneous requests succeed
- **Error rates** — at what load level does n8n start dropping requests
- **Latency distribution** — p50, p95, p99 response times under load
- **Queue behavior** — does n8n queue or reject excess requests

## Three Testing Approaches

### 1. Interactive (Streamlit UI)
Visual interface for ad-hoc testing with real-time results.

### 2. Script-Based (CLI)
Automated testing for CI/CD integration and benchmarking.

### 3. Programmatic (Python API)
Import as a library for custom testing scenarios.

## Architecture

```
Load Tester (async Python)
    ↓ concurrent POST requests
n8n Webhook Endpoint
    ↓ simulated workload (1-5s random)
Response with execution ID + timing
    ↓
Result Correlation & Analysis
```

## Setup

### 1. Import the n8n workflow
```bash
# Import n8n_load_test_workflow.json into your n8n instance
# Activate the workflow (critical!)
# Copy the webhook URL
```

### 2. Configure and run
```bash
cp .env.example .env
# Add your webhook URL to .env
pip install -r requirements.txt
streamlit run app.py
```

## Key Findings

Through systematic testing, this tool reveals n8n's actual concurrency limits — which vary significantly based on:
- Execution mode (main vs. worker)
- Queue configuration
- Workflow complexity
- Infrastructure (self-hosted vs. cloud)

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Testing Engine | Python asyncio + aiohttp |
| UI | Streamlit |
| Analysis | pandas + plotly |
| Target | n8n webhook endpoints |

## Status

Production-ready testing tool. 30 commits of iterative refinement to the testing methodology.
