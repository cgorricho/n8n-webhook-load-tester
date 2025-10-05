import streamlit as st
import asyncio
import aiohttp
import time
from datetime import datetime

st.set_page_config(page_title="n8n Webhook Load Tester", page_icon="🚀", layout="wide")

st.title("🚀 n8n Webhook Load Tester")
st.markdown("Test concurrent webhook executions with async requests")

# Hardcoded webhook URL
WEBHOOK_URL = "https://carlosgorrichoai.one/n8n/webhook-test/load-test"

# Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info(f"**Webhook URL:**\n`{WEBHOOK_URL}`")
    
    num_requests = st.slider(
        "Number of Requests",
        min_value=1,
        max_value=50,
        value=10,
        help="Total number of webhook calls to make"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Status")
    status_placeholder = st.empty()

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Test Controls")
    
with col2:
    st.subheader("Metrics")
    metrics_container = st.container()

# Results area
results_placeholder = st.empty()

async def call_webhook(session, request_id, webhook_url):
    """Make a single async webhook call"""
    start_time = time.time()
    try:
        async with session.post(webhook_url, json={"request_id": request_id}) as response:
            data = await response.json()
            elapsed = time.time() - start_time
            return {
                "request_id": request_id,
                "status": "success",
                "response": data,
                "elapsed_time": round(elapsed, 2),
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "request_id": request_id,
            "status": "error",
            "error": str(e),
            "elapsed_time": round(elapsed, 2),
            "timestamp": datetime.now().isoformat()
        }

async def run_load_test(webhook_url, num_requests, progress_bar, status_text, concurrent_counter):
    """Run the load test with concurrent requests"""
    results = []
    active_requests = 0
    max_concurrent = 0
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for i in range(num_requests):
            task = asyncio.create_task(call_webhook(session, i + 1, webhook_url))
            tasks.append(task)
        
        # Track progress and concurrent executions
        completed = 0
        while tasks:
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED, timeout=0.1)
            
            active_requests = len(pending)
            max_concurrent = max(max_concurrent, active_requests)
            
            # Update UI
            concurrent_counter.metric("🔄 Currently Running", active_requests)
            status_text.info(f"Active requests: {active_requests} | Max concurrent: {max_concurrent}")
            
            for task in done:
                result = await task
                results.append(result)
                completed += 1
                progress_bar.progress(completed / num_requests)
                tasks.remove(task)
    
    return results, max_concurrent

if st.button("🚀 Start Load Test", type="primary", use_container_width=True):
    # Create UI elements
    progress_bar = st.progress(0)
    status_text = status_placeholder.empty()
    
    with metrics_container:
        col_a, col_b = st.columns(2)
        with col_a:
            concurrent_counter = st.empty()
            concurrent_counter.metric("🔄 Currently Running", 0)
        with col_b:
            max_concurrent_display = st.empty()
    
    # Run the load test
    start_time = time.time()
    results, max_concurrent = asyncio.run(
        run_load_test(WEBHOOK_URL, num_requests, progress_bar, status_text, concurrent_counter)
    )
    total_time = time.time() - start_time
    
    # Display final metrics
    concurrent_counter.metric("🔄 Currently Running", 0)
    max_concurrent_display.metric("📈 Max Concurrent", max_concurrent)
    status_text.success(f"✅ Test completed in {total_time:.2f}s")
    
    # Display results
    with results_placeholder.container():
        st.subheader("📊 Results")
        
        # Summary stats
        success_count = sum(1 for r in results if r["status"] == "success")
        error_count = len(results) - success_count
        avg_time = sum(r["elapsed_time"] for r in results) / len(results)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("✅ Successful", success_count)
        col2.metric("❌ Failed", error_count)
        col3.metric("⏱️ Avg Time", f"{avg_time:.2f}s")
        col4.metric("⏰ Total Time", f"{total_time:.2f}s")
        
        # Detailed results table
        st.markdown("### Detailed Results")
        
        # Convert results to a more readable format
        table_data = []
        for r in results:
            if r["status"] == "success":
                response_msg = r["response"].get("message", "N/A")
                workload = r["response"].get("workloadDescription", "N/A")
                execution_id = r["response"].get("executionId", "N/A")
            else:
                response_msg = "Error"
                workload = r.get("error", "Unknown error")
                execution_id = "N/A"
            
            table_data.append({
                "Request ID": r["request_id"],
                "Status": "✅" if r["status"] == "success" else "❌",
                "Execution ID": execution_id,
                "Message": response_msg,
                "Workload": workload,
                "Time (s)": r["elapsed_time"]
            })
        
        st.dataframe(table_data, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("""
### 📝 Instructions
1. **Set the number of requests** using the slider in the sidebar
2. **Click Start Load Test** to begin
3. Watch the real-time concurrent execution counter

### ℹ️ About
This app tests n8n webhook concurrency by making multiple async HTTP requests. 
The workflow has a random 1-5 second delay to simulate real workload and generates 
a unique execution ID for each run based on the timestamp.

**Webhook URL:** `https://carlosgorrichoai.one/n8n/webhook-test/load-test`

**Response Format:**
- `message`: "work complete"
- `executionId`: Unique identifier (e.g., exec-1728095087123-abc123def)
- `delaySeconds`: Random delay (1-5 seconds)
- `workloadDescription`: Human-readable description
""")
