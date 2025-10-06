#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GO_FILE="$SCRIPT_DIR/webhook_loadtest.go"
BINARY_NAME="webhook_load_test"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to show usage
show_usage() {
    echo "🚀 n8n Webhook Load Tester (Go Edition)"
    echo ""
    echo "Usage: $0 <number_of_requests>"
    echo ""
    echo "Arguments:"
    echo "  number_of_requests    Number of concurrent webhook requests to make (1-1000)"
    echo ""
    echo "Examples:"
    echo "  $0 10                 # Test with 10 concurrent requests"
    echo "  $0 50                 # Test with 50 concurrent requests"
    echo "  $0 100                # Test with 100 concurrent requests"
    echo ""
    echo "Features:"
    echo "  - True concurrency using Go routines"
    echo "  - Detailed timing and response analysis"
    echo "  - Real-time statistics"
    echo "  - Comprehensive error reporting"
    echo ""
}

# Function to check if Go is available
check_go() {
    if command -v go >/dev/null 2>&1; then
        print_success "Go found: $(go version)"
        return 0
    else
        print_warning "Go not found locally"
        return 1
    fi
}

# Function to run with local Go
run_with_local_go() {
    print_info "Compiling Go load tester..."
    
    if go build -o "$BINARY_NAME" "$GO_FILE"; then
        print_success "Compilation successful"
        
        print_info "Starting load test with $1 requests..."
        echo ""
        
        # Run the load test
        ./"$BINARY_NAME" "$1"
        
        # Clean up binary
        rm -f "$BINARY_NAME"
        print_info "Cleanup completed"
    else
        print_error "Failed to compile Go program"
        return 1
    fi
}

# Function to run with Docker
run_with_docker() {
    print_info "Running with Docker (official golang image)..."
    
    # Check if Docker is available
    if ! command -v docker >/dev/null 2>&1; then
        print_error "Docker is not available. Please install Docker or Go."
        return 1
    fi
    
    print_info "Pulling official golang Docker image..."
    if ! docker pull golang:1.21-alpine >/dev/null 2>&1; then
        print_error "Failed to pull golang Docker image"
        return 1
    fi
    
    print_success "Docker image ready"
    print_info "Starting load test with $1 requests..."
    echo ""
    
    # Run the load test in Docker
    docker run --rm \
        -v "$SCRIPT_DIR":/app \
        -w /app \
        golang:1.21-alpine \
        sh -c "go run webhook_loadtest.go $1"
}

# Main execution
main() {
    # Check arguments
    if [ $# -ne 1 ]; then
        show_usage
        exit 1
    fi
    
    # Validate number of requests
    if ! [[ "$1" =~ ^[0-9]+$ ]] || [ "$1" -lt 1 ] || [ "$1" -gt 1000 ]; then
        print_error "Invalid number of requests: '$1'"
        print_warning "Must be a number between 1 and 1000"
        echo ""
        show_usage
        exit 1
    fi
    
    print_info "n8n Webhook Load Tester starting..."
    print_info "Target: https://carlosgorrichoai.one/n8n/webhook/load-test"
    print_info "Requests: $1"
    echo ""
    
    # Try local Go first, fall back to Docker
    if check_go; then
        run_with_local_go "$1"
    else
        print_info "Falling back to Docker..."
        run_with_docker "$1"
    fi
}

# Run main function with all arguments
main "$@"
