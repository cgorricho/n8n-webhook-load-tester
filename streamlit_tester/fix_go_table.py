import re

def fix_go_table():
    with open('webhook_loadtest.go', 'r') as f:
        content = f.read()
    
    # Fix the table header
    old_header = 'fmt.Printf("ID  | Status | Time    | Execution ID                    | Workload | Description\\n")'
    new_header = 'fmt.Printf("ID  | Status | Time    | Execution ID                    | Workload | Description\\n")'
    
    # Fix the separator line  
    old_separator = 'fmt.Printf("----+--------+---------+---------------------------------+-------+------------------\\n")'
    new_separator = 'fmt.Printf("----+--------+---------+---------------------------------+----------+---------------------\\n")'
    
    # Fix truncation logic - increase description limit
    old_truncation = '''if len(desc) > 15 {
desc = desc[:12] + "..."
}'''
    new_truncation = '''if len(desc) > 25 {
desc = desc[:22] + "..."
}'''
    
    # Fix printf format string to accommodate wider description column
    old_printf = 'fmt.Printf("%-3d | %s | %7s | %-31s | %-5s | %s\\n",'
    new_printf = 'fmt.Printf("%-3d | %s | %7s | %-31s | %-8s | %s\\n",'
    
    # Apply fixes
    content = content.replace(old_separator, new_separator)
    content = content.replace(old_truncation, new_truncation)
    content = content.replace(old_printf, new_printf)
    
    with open('webhook_loadtest.go', 'w') as f:
        f.write(content)
    
    print("✅ Fixed Go table formatting!")

fix_go_table()
