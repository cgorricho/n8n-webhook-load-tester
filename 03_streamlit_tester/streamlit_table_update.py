import re

def update_streamlit_table():
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find the table_data creation section and replace it
    old_section = '''            table_data = []
            for r in results:
                if r["status"] == "success":
                    response_msg = r["response"].get("message", "N/A")
                    workload = r["response"].get("workloadDescription", "N/A")
                    execution_id = r["response"].get("executionId", "N/A")
                    http_status = r.get("http_status", "N/A")
                else:
                    response_msg = "Error"
                    workload = r.get("error", "Unknown error")
                    execution_id = "N/A"
                    http_status = r.get("http_status", "N/A")
                
                table_data.append({
                    "Request ID": r["request_id"],
                    "Status": "✅" if r["status"] == "success" else "❌",
                    "HTTP Status": http_status,
                    "Execution ID": execution_id,
                    "Message": response_msg,
                    "Workload": workload,
                    "Time (s)": r["elapsed_time"]
                })'''
    
    new_section = '''            table_data = []
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
                })'''
    
    # Replace the section
    updated_content = content.replace(old_section, new_section)
    
    # Write back
    with open('app.py', 'w') as f:
        f.write(updated_content)

update_streamlit_table()
print("✅ Streamlit app table updated!")
