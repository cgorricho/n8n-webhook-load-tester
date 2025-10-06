def add_sorting():
    with open('webhook_loadtest.go', 'r') as f:
        content = f.read()
    
    # Add sort import to the imports section
    old_imports = '''import (
"bytes"
"encoding/json"
"fmt"
"io/ioutil"
"net/http"
"os"
"strconv"
"sync"
"time"
)'''
    
    new_imports = '''import (
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
)'''
    
    # Add sorting logic before printing detailed results
    old_detailed_results = '''// Detailed Results
fmt.Printf("📋 Detailed Request Results:\\n")
fmt.Printf("ID  | Status | Time    | Execution ID                    | Workload | Description\\n")
fmt.Printf("----+--------+---------+---------------------------------+----------+---------------------\\n")

for _, result := range results {'''
    
    new_detailed_results = '''// Sort results by response time (fastest to slowest)
sort.Slice(results, func(i, j int) bool {
return results[i].ResponseTime < results[j].ResponseTime
})

// Detailed Results
fmt.Printf("📋 Detailed Request Results (sorted by response time):\\n")
fmt.Printf("ID  | Status | Time    | Execution ID                    | Workload | Description\\n")
fmt.Printf("----+--------+---------+---------------------------------+----------+---------------------\\n")

for _, result := range results {'''
    
    # Apply changes
    content = content.replace(old_imports, new_imports)
    content = content.replace(old_detailed_results, new_detailed_results)
    
    with open('webhook_loadtest.go', 'w') as f:
        f.write(content)
    
    print("✅ Added response time sorting to Go load tester!")

add_sorting()
