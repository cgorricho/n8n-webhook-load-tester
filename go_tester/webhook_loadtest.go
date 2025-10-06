package main

import (
"bytes"
"encoding/json"
"fmt"
"io/ioutil"
"net/http"
"os"
"sort"
"strconv"
"sync"
"time"
)

// WebhookResponse represents the expected response from n8n webhook
type WebhookResponse struct {
Message             string `json:"message"`
ExecutionID         string `json:"executionId"`
DelaySeconds        int    `json:"delaySeconds"`
StartTime           string `json:"startTime"`
EndTime             string `json:"endTime"`
WorkloadDescription string `json:"workloadDescription"`
}

// RequestResult holds the result of a single webhook request
type RequestResult struct {
RequestID    int                  `json:"requestId"`
Success      bool                 `json:"success"`
StatusCode   int                  `json:"statusCode"`
ResponseTime time.Duration        `json:"responseTime"`
Response     *WebhookResponse     `json:"response,omitempty"`
Error        string              `json:"error,omitempty"`
Timestamp    time.Time           `json:"timestamp"`
}

// TestStats holds overall test statistics
type TestStats struct {
TotalRequests   int           `json:"totalRequests"`
SuccessfulReqs  int           `json:"successfulRequests"`
FailedReqs      int           `json:"failedRequests"`
TotalDuration   time.Duration `json:"totalDuration"`
AvgResponseTime time.Duration `json:"averageResponseTime"`
MaxResponseTime time.Duration `json:"maxResponseTime"`
MinResponseTime time.Duration `json:"minResponseTime"`
RequestsPerSec  float64       `json:"requestsPerSecond"`
}

const webhookURL = "https://carlosgorrichoai.one/n8n/webhook/load-test"

func main() {
if len(os.Args) != 2 {
fmt.Printf("Usage: %s <number_of_requests>\n", os.Args[0])
fmt.Printf("Example: %s 10\n", os.Args[0])
os.Exit(1)
}

numRequests, err := strconv.Atoi(os.Args[1])
if err != nil || numRequests < 1 {
fmt.Printf("Error: Invalid number of requests '%s'. Must be a positive integer.\n", os.Args[1])
os.Exit(1)
}

fmt.Printf("🚀 Starting n8n Webhook Load Test\n")
fmt.Printf("📊 Configuration:\n")
fmt.Printf("   - Target URL: %s\n", webhookURL)
fmt.Printf("   - Total Requests: %d\n", numRequests)
fmt.Printf("   - Concurrency: All requests launched simultaneously\n\n")

// Run the load test
results, stats := runLoadTest(numRequests)

// Print results
printResults(results, stats)
}

func runLoadTest(numRequests int) ([]RequestResult, TestStats) {
var wg sync.WaitGroup
results := make([]RequestResult, numRequests)

startTime := time.Now()
fmt.Printf("⏱️  Test started at: %s\n\n", startTime.Format("2006-01-02 15:04:05"))

// Launch all requests concurrently
for i := 0; i < numRequests; i++ {
wg.Add(1)
go func(requestID int) {
defer wg.Done()
results[requestID] = makeRequest(requestID + 1)
}(i)
}

// Wait for all requests to complete
wg.Wait()
totalDuration := time.Since(startTime)

// Calculate statistics
stats := calculateStats(results, totalDuration)

return results, stats
}

func makeRequest(requestID int) RequestResult {
result := RequestResult{
RequestID: requestID,
Timestamp: time.Now(),
}

// Prepare request payload
payload := map[string]interface{}{
"request_id": requestID,
"test":       true,
"timestamp":  result.Timestamp.Unix(),
}

jsonData, err := json.Marshal(payload)
if err != nil {
result.Success = false
result.Error = fmt.Sprintf("JSON marshal error: %v", err)
return result
}

// Make HTTP request
requestStart := time.Now()

resp, err := http.Post(webhookURL, "application/json", bytes.NewBuffer(jsonData))
if err != nil {
result.Success = false
result.Error = fmt.Sprintf("HTTP request failed: %v", err)
result.ResponseTime = time.Since(requestStart)
return result
}
defer resp.Body.Close()

result.ResponseTime = time.Since(requestStart)
result.StatusCode = resp.StatusCode

// Read response body
body, err := ioutil.ReadAll(resp.Body)
if err != nil {
result.Success = false
result.Error = fmt.Sprintf("Failed to read response body: %v", err)
return result
}

// Check if request was successful
if resp.StatusCode == 200 {
// Try to parse webhook response
var webhookResp WebhookResponse
if err := json.Unmarshal(body, &webhookResp); err == nil {
result.Success = true
result.Response = &webhookResp
} else {
result.Success = false
result.Error = fmt.Sprintf("Failed to parse webhook response: %v", err)
}
} else {
result.Success = false
result.Error = fmt.Sprintf("HTTP %d: %s", resp.StatusCode, string(body))
}

return result
}

func calculateStats(results []RequestResult, totalDuration time.Duration) TestStats {
stats := TestStats{
TotalRequests: len(results),
TotalDuration: totalDuration,
MinResponseTime: time.Hour, // Initialize to high value
}

var totalResponseTime time.Duration

for _, result := range results {
totalResponseTime += result.ResponseTime

if result.Success {
stats.SuccessfulReqs++
} else {
stats.FailedReqs++
}

// Track min/max response times
if result.ResponseTime > stats.MaxResponseTime {
stats.MaxResponseTime = result.ResponseTime
}
if result.ResponseTime < stats.MinResponseTime {
stats.MinResponseTime = result.ResponseTime
}
}

// Calculate averages
if len(results) > 0 {
stats.AvgResponseTime = totalResponseTime / time.Duration(len(results))
stats.RequestsPerSec = float64(len(results)) / totalDuration.Seconds()
}

if stats.MinResponseTime == time.Hour {
stats.MinResponseTime = 0 // No successful requests
}

return stats
}

func printResults(results []RequestResult, stats TestStats) {
fmt.Printf("📈 LOAD TEST RESULTS\n")
fmt.Printf("==========================================\n\n")

// Overall Statistics
fmt.Printf("📊 Overall Statistics:\n")
fmt.Printf("   Total Requests:     %d\n", stats.TotalRequests)
fmt.Printf("   Successful:         %d (%.1f%%)\n", stats.SuccessfulReqs, float64(stats.SuccessfulReqs)/float64(stats.TotalRequests)*100)
fmt.Printf("   Failed:             %d (%.1f%%)\n", stats.FailedReqs, float64(stats.FailedReqs)/float64(stats.TotalRequests)*100)
fmt.Printf("   Total Duration:     %v\n", stats.TotalDuration)
fmt.Printf("   Requests/Second:    %.2f\n\n", stats.RequestsPerSec)

// Response Time Statistics
fmt.Printf("⏱️  Response Time Statistics:\n")
fmt.Printf("   Average:            %v\n", stats.AvgResponseTime)
fmt.Printf("   Minimum:            %v\n", stats.MinResponseTime)
fmt.Printf("   Maximum:            %v\n\n", stats.MaxResponseTime)

// Sort results by response time (fastest to slowest)
sort.Slice(results, func(i, j int) bool {
return results[i].ResponseTime < results[j].ResponseTime
})

// Detailed Results
fmt.Printf("📋 Detailed Request Results (sorted by response time):\n")
fmt.Printf("ID  | Status | Time    | Execution ID                    | Workload | Description\n")
fmt.Printf("----+--------+---------+---------------------------------+----------+---------------------\n")

for _, result := range results {
status := "❌ FAIL"
execID := "N/A"
workload := "N/A"
desc := "N/A"

if result.Success && result.Response != nil {
status = "✅ OK  "
execID = result.Response.ExecutionID
if len(execID) > 28 {
execID = execID[:28] + "..."
}
workload = fmt.Sprintf("%ds", result.Response.DelaySeconds)
desc = result.Response.WorkloadDescription
if len(desc) > 25 {
desc = desc[:22] + "..."
}
}

fmt.Printf("%-3d | %s | %7s | %-31s | %-8s | %s\n",
result.RequestID,
status,
formatDuration(result.ResponseTime),
execID,
workload,
desc,
)
}

// Error Summary (if any failures)
if stats.FailedReqs > 0 {
fmt.Printf("\n🚨 Error Summary:\n")
for _, result := range results {
if !result.Success {
fmt.Printf("   Request %d: %s\n", result.RequestID, result.Error)
}
}
}

fmt.Printf("\n🎯 Test completed successfully!\n")
}

func formatDuration(d time.Duration) string {
if d < time.Millisecond {
return fmt.Sprintf("%dµs", d.Microseconds())
} else if d < time.Second {
return fmt.Sprintf("%dms", d.Milliseconds())
} else {
return fmt.Sprintf("%.1fs", d.Seconds())
}
}
