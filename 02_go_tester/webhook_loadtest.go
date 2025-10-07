package main

import (
"bytes"
"encoding/json"
"fmt"
"log"
"math/rand"
"net/http"
"os"
"strconv"
"sync"
"time"

"github.com/joho/godotenv"
)

type WebhookPayload struct {
Message     string `json:"message"`
WorkloadSec int    `json:"workload_sec"`
Timestamp   string `json:"timestamp"`
}

type LoadTestResult struct {
ConcurrentRequests  int           `json:"concurrent_requests"`
RequestID           int           `json:"request_id"`
ResponseTimeSeconds float64       `json:"response_time_seconds"`
WorkloadSeconds     int           `json:"workload_seconds"`
ExecutionID         string        `json:"execution_id"`
Status              string        `json:"status"`
Timestamp           string        `json:"timestamp"`
HTTPStatus          int           `json:"http_status"`
}

type N8nResponse struct {
ExecutionID string `json:"executionId"`
Message     string `json:"message"`
Status      string `json:"status"`
}

var webhookURL string

func loadEnv() {
// Try to load .env file
err := godotenv.Load("../.env")
if err != nil {
// If .env doesn't exist, try current directory
err = godotenv.Load(".env")
if err != nil {
log.Printf("Warning: .env file not found, using environment variables directly")
}
}

// Get webhook URL from environment
webhookURL = os.Getenv("N8N_WEBHOOK_URL")
if webhookURL == "" {
log.Fatal("N8N_WEBHOOK_URL environment variable is required. Please create a .env file with N8N_WEBHOOK_URL=your-webhook-url")
}

fmt.Printf("🔗 Using webhook URL: %s\n", webhookURL)
}

func main() {
// Load environment variables
loadEnv()

if len(os.Args) < 2 {
fmt.Println("Usage: go run webhook_loadtest.go <concurrent_requests>")
fmt.Println("Example: go run webhook_loadtest.go 10")
return
}

concurrentRequests, err := strconv.Atoi(os.Args[1])
if err != nil {
log.Fatal("Invalid number of concurrent requests")
}

fmt.Printf("🚀 Starting load test with %d concurrent requests\n", concurrentRequests)
fmt.Printf("🎯 Target: %s\n", webhookURL)

results := make(chan LoadTestResult, concurrentRequests)
var wg sync.WaitGroup

startTime := time.Now()

for i := 1; i <= concurrentRequests; i++ {
wg.Add(1)
go func(requestID int) {
defer wg.Done()

workloadSec := rand.Intn(5) + 1 // Random workload 1-5 seconds

result := LoadTestResult{
ConcurrentRequests: concurrentRequests,
RequestID:          requestID,
WorkloadSeconds:    workloadSec,
Timestamp:          time.Now().Format(time.RFC3339),
}

// Make the webhook request
requestStart := time.Now()
executionID, httpStatus, err := makeWebhookRequest(workloadSec)
requestDuration := time.Since(requestStart)

result.ResponseTimeSeconds = requestDuration.Seconds()
result.HTTPStatus = httpStatus

if err != nil {
result.Status = "ERROR"
result.ExecutionID = fmt.Sprintf("error: %v", err)
fmt.Printf("❌ Request %d failed: %v\n", requestID, err)
} else {
result.Status = "SUCCESS"
result.ExecutionID = executionID
fmt.Printf("✅ Request %d completed in %.2fs (workload: %ds, execution: %s)\n",
requestID, requestDuration.Seconds(), workloadSec, executionID)
}

results <- result
}(i)
}

go func() {
wg.Wait()
close(results)
}()

// Collect results
var allResults []LoadTestResult
for result := range results {
allResults = append(allResults, result)
}

totalDuration := time.Since(startTime)

// Print summary
fmt.Printf("\n📊 Load Test Summary:\n")
fmt.Printf("Total time: %.2f seconds\n", totalDuration.Seconds())
fmt.Printf("Concurrent requests: %d\n", concurrentRequests)

successCount := 0
totalResponseTime := 0.0
totalWorkloadTime := 0.0

for _, result := range allResults {
if result.Status == "SUCCESS" {
successCount++
totalResponseTime += result.ResponseTimeSeconds
totalWorkloadTime += float64(result.WorkloadSeconds)
}
}

if successCount > 0 {
avgResponseTime := totalResponseTime / float64(successCount)
avgWorkloadTime := totalWorkloadTime / float64(successCount)
processingOverhead := ((avgResponseTime - avgWorkloadTime) / avgWorkloadTime) * 100

fmt.Printf("Success rate: %.1f%% (%d/%d)\n", float64(successCount)/float64(concurrentRequests)*100, successCount, concurrentRequests)
fmt.Printf("Average response time: %.2f seconds\n", avgResponseTime)
fmt.Printf("Average workload time: %.2f seconds\n", avgWorkloadTime)
fmt.Printf("Processing overhead: +%.1f%%\n", processingOverhead)
}

// Save results to CSV
saveResultsToCSV(allResults)
}

func makeWebhookRequest(workloadSec int) (string, int, error) {
payload := WebhookPayload{
Message:     fmt.Sprintf("Load test request - workload %d seconds", workloadSec),
WorkloadSec: workloadSec,
Timestamp:   time.Now().Format(time.RFC3339),
}

jsonData, err := json.Marshal(payload)
if err != nil {
return "", 0, err
}

resp, err := http.Post(webhookURL, "application/json", bytes.NewBuffer(jsonData))
if err != nil {
return "", 0, err
}
defer resp.Body.Close()

var n8nResp N8nResponse
if err := json.NewDecoder(resp.Body).Decode(&n8nResp); err != nil {
return "", resp.StatusCode, fmt.Errorf("failed to decode response: %v", err)
}

return n8nResp.ExecutionID, resp.StatusCode, nil
}

func saveResultsToCSV(results []LoadTestResult) {
filename := fmt.Sprintf("./results/go_load_test_%s.csv", time.Now().Format("2006-01-02_15-04-05"))

// Create results directory if it doesn't exist
if err := os.MkdirAll("./results", 0755); err != nil {
log.Printf("Warning: Could not create results directory: %v", err)
return
}

file, err := os.Create(filename)
if err != nil {
log.Printf("Warning: Could not create CSV file: %v", err)
return
}
defer file.Close()

// Write CSV header
fmt.Fprintf(file, "concurrent_requests,request_id,response_time_seconds,workload_seconds,execution_id,status,timestamp,http_status\n")

// Write results
for _, result := range results {
fmt.Fprintf(file, "%d,%d,%.3f,%d,%s,%s,%s,%d\n",
result.ConcurrentRequests,
result.RequestID,
result.ResponseTimeSeconds,
result.WorkloadSeconds,
result.ExecutionID,
result.Status,
result.Timestamp,
result.HTTPStatus)
}

fmt.Printf("💾 Results saved to: %s\n", filename)
}
