import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read the CSV data
df = pd.read_csv('article_assets/data/n8n_concurrency_test_results.csv')

# CONSISTENT BLUE COLOR SCHEME - Same as hero chart
blue_colors = [
    '#87CEEB',  # Light blue (5 requests)
    '#4682B4',  # Steel blue (10 requests)  
    '#1E90FF',  # Dodger blue (20 requests)
    '#000080'   # Navy blue (30 requests)
]

concurrent_levels = [5, 10, 20, 30]

print("🔧 Fixing queueing evidence chart issues...")
print("Issues to fix:")
print("1. Title overlapping with subplot titles")
print("2. Reindex iterations to start at 1")
print("3. Integer iteration labels only")
print("4. Add workload values inside bars")

# Chart 4: Queueing Evidence (Response Time Patterns) - FIXED VERSION
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
sns.set_style("whitegrid")

axes = [ax1, ax2, ax3, ax4]

for i, level in enumerate(concurrent_levels):
    ax = axes[i]
    level_data = df[df['concurrent_requests'] == level].copy()
    level_data = level_data.sort_values('response_time_seconds').reset_index(drop=True)
    
    # REINDEX: Start at 1 instead of 0
    iterations = range(1, len(level_data) + 1)
    
    # Plot response times with REINDEXED x-axis
    bars = ax.bar(iterations, level_data['response_time_seconds'], 
                  color=blue_colors[i], alpha=0.8)
    
    # ADD WORKLOAD VALUES INSIDE BARS
    for j, (bar, workload) in enumerate(zip(bars, level_data['workload_seconds'])):
        height = bar.get_height()
        # Place text in the middle of each bar
        ax.text(bar.get_x() + bar.get_width()/2., height/2, 
                f'{int(workload)}s', 
                ha='center', va='center', 
                fontweight='bold', 
                fontsize=9,
                color='white' if blue_colors[i] == '#000080' else 'black')
    
    # Add workload reference line
    avg_workload = level_data['workload_seconds'].mean()
    ax.axhline(y=avg_workload, color='#FF6347', linestyle='--', linewidth=2, 
               label=f'Avg Workload ({avg_workload:.1f}s)')
    
    ax.set_title(f'{level} Concurrent Requests\nSorted by Response Time', 
                fontweight='bold', fontsize=12)
    ax.set_xlabel('Request (Sorted by Response Time)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Response time (seconds)', fontsize=10, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # FORCE INTEGER LABELS ON X-AXIS
    ax.set_xticks(iterations)
    ax.set_xticklabels([str(x) for x in iterations])
    
    # Highlight queueing pattern
    if len(level_data) > 5:
        first_half = level_data.iloc[:len(level_data)//2]['response_time_seconds'].mean()
        second_half = level_data.iloc[len(level_data)//2:]['response_time_seconds'].mean()
        queueing_effect = second_half - first_half
        
        ax.text(0.02, 0.98, f'Queueing Effect:\n+{queueing_effect:.1f}s average\nfor later requests', 
                transform=ax.transAxes, fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='#F0F8FF', alpha=0.9, edgecolor='#4682B4'))

# FIXED MAIN TITLE POSITIONING - More space from subplot titles
plt.suptitle('n8n Queueing Evidence: Response Time Patterns', 
             fontsize=16, fontweight='bold', y=0.98)  # Increased y from 0.95 to 0.98

# ADJUSTED LAYOUT to prevent title overlap
plt.tight_layout(rect=[0, 0, 1, 0.94])  # Leave more space at top for title

plt.savefig('article_assets/images/n8n_queueing_evidence.png', 
            dpi=300, bbox_inches='tight', facecolor='white')

print("✅ Fixed queueing evidence chart!")
print("🔧 Fixes applied:")
print("   ✓ Main title positioned higher to avoid overlap")
print("   ✓ Iterations reindexed to start at 1")  
print("   ✓ X-axis labels forced to integers only")
print("   ✓ Workload values added inside each bar")
print("   ✓ Text color adjusted for visibility on dark bars")
print("   ✓ Maintained consistent blue color scheme")

plt.show()

# Verify the data
print(f"\n📊 Data verification:")
for level in concurrent_levels:
    level_data = df[df['concurrent_requests'] == level]
    print(f"   Concurrency {level}: {len(level_data)} requests, workloads: {sorted(level_data['workload_seconds'].unique())}")
