#!/usr/bin/env python3

# Read the original article content
with open('article_assets/medium_article_draft_improved_original.md', 'r') as f:
    content = f.read()

# Replace the flat text architecture diagram with a simple Mermaid equivalent
old_diagram = '''```
Webhook Request → n8n Web Server → Task Broker → Task Runner Pool
       ↓               ↓               ↓              ↓
   Unlimited      Creates Record    Internal Queue   ~5 Workers
```'''

new_diagram = '''```mermaid
flowchart LR
    A[Webhook Request] --> B[n8n Web Server]
    B --> C[Task Broker]
    C --> D[Task Runner Pool]
    
    A1[Unlimited] -.-> A
    B1[Creates Record] -.-> B
    C1[Internal Queue] -.-> C
    D1[~5 Workers] -.-> D
```'''

# Replace the diagram
content = content.replace(old_diagram, new_diagram)

# Save the updated content
with open('article_assets/medium_article_draft_improved.md', 'w') as f:
    f.write(content)

print("✅ Updated article with simple Mermaid diagram that matches the original style!")
print("📏 Replaced complex flowcharts with clean, minimal diagram")
