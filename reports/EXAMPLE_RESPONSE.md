# Example Response

When you invoke the n8n webhook, you'll receive a response like this:

```json
{
  "message": "work complete",
  "executionId": "exec-1728095087123-x9k2m7p4q",
  "delaySeconds": 3,
  "startTime": "2025-10-05T02:34:52.287Z",
  "endTime": "2025-10-05T02:34:55.287Z",
  "workloadDescription": "Simulated 3s workload"
}
```

## Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `message` | string | Always "work complete" to indicate successful execution |
| `executionId` | string | Unique identifier for this execution (format: `exec-{timestamp}-{random}`) |
| `delaySeconds` | number | Random delay between 1-5 seconds used for this execution |
| `startTime` | string | ISO 8601 timestamp when the workflow execution started |
| `endTime` | string | ISO 8601 timestamp when the workflow execution completed |
| `workloadDescription` | string | Human-readable description of the simulated workload |

## Execution ID Format

The `executionId` is generated using this pattern:
- **Prefix**: `exec-`
- **Timestamp**: Milliseconds since epoch (e.g., `1728095087123`)
- **Random suffix**: 9-character random alphanumeric string (e.g., `x9k2m7p4q`)

**Example**: `exec-1728095087123-x9k2m7p4q`

This ensures each execution has a globally unique identifier even if multiple executions start at the exact same millisecond.

## Testing with curl

```bash
curl -X POST "https://your-n8n-instance.com/webhook/load-test" \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

Expected response (example):
```json
{
  "message": "work complete",
  "executionId": "exec-1728095124567-a3b4c5d6e",
  "delaySeconds": 2,
  "startTime": "2025-10-05T02:45:24.567Z",
  "endTime": "2025-10-05T02:45:26.567Z",
  "workloadDescription": "Simulated 2s workload"
}
```
