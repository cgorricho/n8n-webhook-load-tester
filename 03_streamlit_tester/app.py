import streamlit as st
import asyncio
import aiohttp
import time
from datetime import datetime
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('webhook_tester.log')
    ]
)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="n8n Webhook Load Tester", page_icon="🚀", layout="wide")

st.title("🚀 n8n Webhook Load Tester")
st.markdown("Test concurrent webhook executions with async requests")

# Hardcoded webhook URL - using external domain for production access
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
if not WEBHOOK_URL:
    st.error("N8N_WEBHOOK_URL environment variable not found! Please create a .env file.")
    st.stop()

logger.info(f"App started. Webhook URL: {WEBHOOK_URL}")

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
    
    # Show log file location
    st.markdown("---")
    st.markdown("### 🐛 Debug")
    st.caption("Logs written to: `webhook_tester.log`")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Test Controls")
    
with col2:
    st.subheader("Metrics")
    metrics_container = st.container()

# Results area
results_placeholder = st.empty()
debug_placeholder = st.empty()

async def call_webhook(session, request_id, webhook_url):
    """Make a single async webhook call"""
    logger.debug(f"Request {request_id}: Starting webhook call to {webhook_url}")
    start_time = time.time()
    
    try:
        logger.debug(f"Request {request_id}: Initiating POST request")
        async with session.post(
            webhook_url, 
            json={"request_id": request_id},
            timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            logger.debug(f"Request {request_id}: Received response - Status: {response.status}")
            logger.debug(f"Request {request_id}: Response headers: {dict(response.headers)}")
            
            # Get response text first for debugging
            response_text = await response.text()
            logger.debug(f"Request {request_id}: Response body (raw): {response_text[:200]}...")
            
            # Try to parse as JSON
            try:
                data = await response.json()
                logger.info(f"Request {request_id}: Successfully parsed JSON response")
            except Exception as json_error:
                logger.error(f"Request {request_id}: Failed to parse JSON: {json_error}")
                logger.error(f"Request {request_id}: Full response text: {response_text}")
                data = {"error": "Invalid JSON response", "raw_response": response_text}
            
            elapsed = time.time() - start_time
            logger.info(f"Request {request_id}: Completed successfully in {elapsed:.2f}s")
            
            return {
                "request_id": request_id,
                "status": "success" if response.status == 200 else "error",
                "http_status": response.status,
                "response": data,
                "elapsed_time": round(elapsed, 2),
                "timestamp": datetime.now().isoformat()
            }
            
    except asyncio.TimeoutError as e:
        elapsed = time.time() - start_time
        logger.error(f"Request {request_id}: Timeout error after {elapsed:.2f}s: {e}")
        return {
            "request_id": request_id,
            "status": "error",
            "error": f"Timeout after {elapsed:.2f}s",
            "elapsed_time": round(elapsed, 2),
            "timestamp": datetime.now().isoformat()
        }
        
    except aiohttp.ClientError as e:
        elapsed = time.time() - start_time
        logger.error(f"Request {request_id}: Client error: {type(e).__name__}: {e}")
        return {
            "request_id": request_id,
            "status": "error",
            "error": f"Client error: {type(e).__name__}: {str(e)}",
            "elapsed_time": round(elapsed, 2),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Request {request_id}: Unexpected error: {type(e).__name__}: {e}", exc_info=True)
        return {
            "request_id": request_id,
            "status": "error",
            "error": f"Unexpected error: {type(e).__name__}: {str(e)}",
            "elapsed_time": round(elapsed, 2),
            "timestamp": datetime.now().isoformat()
        }

async def run_load_test(webhook_url, num_requests, progress_bar, status_text, concurrent_counter):
    """Run the load test with concurrent requests"""
    logger.info(f"Starting load test with {num_requests} requests to {webhook_url}")
    results = []
    active_requests = 0
    max_concurrent = 0
    
    try:
        logger.debug("Creating aiohttp ClientSession")
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            logger.debug(f"Creating {num_requests} async tasks")
            for i in range(num_requests):
                task = asyncio.create_task(call_webhook(session, i + 1, webhook_url))
                tasks.append(task)
            
            logger.info(f"All {num_requests} tasks created, starting execution")
            
            # Track progress and concurrent executions
            completed = 0
            while tasks:
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED, timeout=0.1)
                
                active_requests = len(pending)
                max_concurrent = max(max_concurrent, active_requests)
                
                if done:
                    logger.debug(f"Batch completed: {len(done)} tasks finished. Pending: {active_requests}")
                
                # Update UI
                concurrent_counter.metric("🔄 Currently Running", active_requests)
                status_text.info(f"Active requests: {active_requests} | Max concurrent: {max_concurrent}")
                
                for task in done:
                    result = await task
                    results.append(result)
                    completed += 1
                    progress_bar.progress(completed / num_requests)
                    tasks.remove(task)
                    
                    # Log result summary
                    if result["status"] == "success":
                        logger.info(f"Request {result['request_id']}: SUCCESS")
                    else:
                        logger.warning(f"Request {result['request_id']}: FAILED - {result.get('error', 'Unknown error')}")
        
        logger.info(f"Load test completed. Success: {sum(1 for r in results if r['status'] == 'success')}/{num_requests}")
        return results, max_concurrent
        
    except Exception as e:
        logger.error(f"Load test failed with error: {type(e).__name__}: {e}", exc_info=True)
        raise

if st.button("🚀 Start Load Test", type="primary", use_container_width=True):
    logger.info("=== LOAD TEST STARTED ===")
    logger.info(f"Configuration: {num_requests} requests to {WEBHOOK_URL}")
    
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
    
    try:
        # Run the load test
        start_time = time.time()
        results, max_concurrent = asyncio.run(
            run_load_test(WEBHOOK_URL, num_requests, progress_bar, status_text, concurrent_counter)
        )
        total_time = time.time() - start_time
        
        logger.info(f"=== LOAD TEST COMPLETED === Total time: {total_time:.2f}s")
        
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
            
            # Show debug info if there were errors
            if error_count > 0:
                with st.expander("🐛 Debug Information (Errors Found)", expanded=True):
                    for r in results:
                        if r["status"] == "error":
                            st.error(f"**Request {r['request_id']}:** {r.get('error', 'Unknown error')}")
                            if "http_status" in r:
                                st.write(f"HTTP Status: {r['http_status']}")
                            if "response" in r:
                                st.json(r["response"])
            
            # Detailed results table
            st.markdown("### Detailed Results")
            
            # Convert results to a more readable format
            table_data = []
            for r in results:
                if r["status"] == "success":
                    response_msg = r["response"].get("message", "N/A")
                    execution_id = r["response"].get("executionId", "N/A")
                    http_status = r.get("http_status", "N/A")
                    
                    # Extract workload delay from n8n response
                    workload_seconds = r["response"].get("delaySeconds", 0)
                    workload_desc = r["response"].get("workloadDescription", "N/A")
                    
                    # Format workload display like Go version
                    if workload_seconds > 0:
                        workload_display = f"{workload_seconds}s"
                    else:
                        workload_display = "N/A"
                        
                else:
                    response_msg = "Error"
                    workload_display = "N/A"
                    workload_desc = r.get("error", "Unknown error")
                    execution_id = "N/A"
                    http_status = r.get("http_status", "N/A")
                
                # Format response time like Go version (with better precision)
                response_time = f"{r['elapsed_time']:.2f}s"
                
                table_data.append({
                    "ID": r["request_id"],
                    "Status": "✅" if r["status"] == "success" else "❌",
                    "Response Time": response_time,
                    "Execution ID": execution_id,
                    "Workload": workload_display,
                    "Description": workload_desc,
                    "HTTP": http_status
                })
            
            st.dataframe(table_data, use_container_width=True, hide_index=True)
            
    except Exception as e:
        logger.error(f"Fatal error during load test: {type(e).__name__}: {e}", exc_info=True)
        st.error(f"❌ Fatal error: {type(e).__name__}: {str(e)}")
        st.error("Check `webhook_tester.log` for detailed error information")

st.markdown("---")
st.markdown("""
### 📝 Instructions
1. **Ensure the n8n workflow is ACTIVE** (toggle must be ON)
2. **Set the number of requests** using the slider in the sidebar
3. **Click Start Load Test** to begin
4. Watch the real-time concurrent execution counter
5. Check `webhook_tester.log` for detailed debugging information

### ℹ️ About
This app tests n8n webhook concurrency by making multiple async HTTP requests. 
The workflow has a random 1-5 second delay to simulate real workload and generates 
a unique execution ID for each run based on the timestamp.

**Webhook URL:** Configured via .env file (external production endpoint)

**Response Format:**
- `message`: "work complete"
- `executionId`: Unique identifier (e.g., exec-1728095087123-abc123def)
- `delaySeconds`: Random delay (1-5 seconds)
- `workloadDescription`: Human-readable description
""")
