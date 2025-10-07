#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Read the data
df = pd.read_csv('article_assets/data/n8n_concurrency_test_results.csv')

# CONSISTENT BLUE COLOR SCHEME - Same as hero chart
blue_colors = [
    '#87CEEB',  # Light blue (5 requests)
    '#4682B4',  # Steel blue (10 requests)  
    '#1E90FF',  # Dodger blue (20 requests)
    '#000080'   # Navy blue (30 requests)
]

concurrent_levels = [5, 10, 20, 30]
color_map = dict(zip(concurrent_levels, blue_colors))

print("🎨 Creating all charts with consistent blue color scheme...")
print("Colors: Light Blue → Steel Blue → Dodger Blue → Navy Blue")

# ===============================
# Chart 1: Response Time Distribution (Box Plot)
# ===============================
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

df_grouped = []
labels = []
for level in concurrent_levels:
    level_data = df[df['concurrent_requests'] == level]['response_time_seconds']
    df_grouped.append(level_data)
    labels.append(f'{level} Concurrent')

box_plot = plt.boxplot(df_grouped, tick_labels=labels, patch_artist=True)
for patch, color in zip(box_plot['boxes'], blue_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)

# Style whiskers and other elements
for element in ['whiskers', 'fliers', 'medians', 'caps']:
    for item in box_plot[element]:
        item.set_color('#2F4F4F')  # Dark slate gray
        if element == 'medians':
            item.set_linewidth(2)

plt.ylabel('Response Time (seconds)', fontsize=14, fontweight='bold')
plt.xlabel('Concurrency Level', fontsize=14, fontweight='bold')
plt.title('n8n Response Time Distribution by Concurrency Level', 
          fontsize=16, fontweight='bold', pad=20)
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('article_assets/images/n8n_response_distribution.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Updated Chart 1: n8n_response_distribution.png")
plt.show()

# ===============================
# Chart 2: Processing Overhead Analysis (Stacked Bar)
# ===============================
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

summary_data = []
for level in concurrent_levels:
    level_data = df[df['concurrent_requests'] == level]
    avg_response = level_data['response_time_seconds'].mean()
    avg_workload = level_data['workload_seconds'].mean()
    overhead = avg_response - avg_workload
    summary_data.append({
        'concurrent_requests': level,
        'avg_response_time': avg_response,
        'avg_workload': avg_workload,
        'overhead': overhead
    })

summary_df = pd.DataFrame(summary_data)

width = 0.6
x_pos = range(len(concurrent_levels))

# Use blue theme for stacked bars
bars1 = plt.bar(x_pos, summary_df['avg_workload'], width, label='Average Workload Time', 
                color='#B0E0E6', alpha=0.9)  # Light steel blue
bars2 = plt.bar(x_pos, summary_df['overhead'], width, 
                bottom=summary_df['avg_workload'], label='Processing Overhead', 
                color='#4169E1', alpha=0.9)  # Royal blue

# Add value labels on bars
for i, (workload, overhead, total) in enumerate(zip(summary_df['avg_workload'], 
                                                   summary_df['overhead'], 
                                                   summary_df['avg_response_time'])):
    plt.text(i, total + 0.1, f'{total:.1f}s\ntotal', ha='center', va='bottom', fontweight='bold')
    overhead_pct = (overhead / workload) * 100
    plt.text(i, workload + overhead/2, f'+{overhead_pct:.0f}%', ha='center', va='center', 
             fontweight='bold', color='white', fontsize=11)

plt.xlabel('Concurrent Requests', fontsize=14, fontweight='bold')
plt.ylabel('Time (seconds)', fontsize=14, fontweight='bold')
plt.title('n8n Processing Overhead Growth', 
          fontsize=16, fontweight='bold', pad=20)
plt.xticks(x_pos, concurrent_levels)
plt.legend(loc='upper left')
plt.grid(True, linestyle=':', alpha=0.6, axis='y')
plt.tight_layout()

plt.savefig('article_assets/images/n8n_processing_overhead.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Updated Chart 2: n8n_processing_overhead.png")
plt.show()

# ===============================
# Chart 3: Throughput Analysis
# ===============================
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

# Calculate metrics for each level
metrics_data = []
for level in concurrent_levels:
    level_data = df[df['concurrent_requests'] == level]
    success_count = len(level_data)
    success_rate = (success_count / level) * 100
    avg_response = level_data['response_time_seconds'].mean()
    theoretical_throughput = level / avg_response
    
    metrics_data.append({
        'concurrent_requests': level,
        'success_rate': success_rate,
        'theoretical_throughput': theoretical_throughput,
        'avg_response_time': avg_response
    })

metrics_df = pd.DataFrame(metrics_data)

# Dual y-axis plot with blue theme
fig, ax1 = plt.subplots(figsize=(12, 8))
ax2 = ax1.twinx()

# Plot success rate as bars in blue gradient
bars = ax1.bar(concurrent_levels, metrics_df['success_rate'], 
               alpha=0.8, color=blue_colors, width=2)
ax1.set_ylabel('Success Rate (%)', fontsize=14, fontweight='bold', color='#000080')
ax1.set_ylim(0, 110)

# Plot throughput as line in dark blue
line = ax2.plot(concurrent_levels, metrics_df['theoretical_throughput'], 
                'o-', linewidth=3, markersize=12, label='Theoretical Max Throughput',
                color='#191970', markerfacecolor='#4169E1', markeredgecolor='white', markeredgewidth=2)
ax2.set_ylabel('Theoretical Throughput (requests/second)', fontsize=14, fontweight='bold', color='#191970')

ax1.set_xlabel('Concurrent Requests', fontsize=14, fontweight='bold')
plt.title('n8n Success Rate vs Theoretical Throughput', 
          fontsize=16, fontweight='bold', pad=20)

# Add value labels
for i, (bar, rate, throughput) in enumerate(zip(bars, metrics_df['success_rate'], 
                                               metrics_df['theoretical_throughput'])):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'{rate:.0f}%', ha='center', va='bottom', fontweight='bold', color='#000080')
    ax2.text(concurrent_levels[i], throughput + 0.2, f'{throughput:.1f}', 
             ha='center', va='bottom', fontweight='bold', color='#191970')

ax1.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()

plt.savefig('article_assets/images/n8n_throughput_analysis.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Updated Chart 3: n8n_throughput_analysis.png")
plt.show()

# ===============================
# Chart 4: Queueing Evidence (Response Time Patterns)
# ===============================
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
sns.set_style("whitegrid")

axes = [ax1, ax2, ax3, ax4]

for i, level in enumerate(concurrent_levels):
    ax = axes[i]
    level_data = df[df['concurrent_requests'] == level].copy()
    level_data = level_data.sort_values('response_time_seconds').reset_index()
    
    # Plot response times in order with blue gradient
    bars = ax.bar(range(len(level_data)), level_data['response_time_seconds'], 
                  color=blue_colors[i], alpha=0.8)
    
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
    
    # Highlight queueing pattern
    if len(level_data) > 5:
        first_half = level_data.iloc[:len(level_data)//2]['response_time_seconds'].mean()
        second_half = level_data.iloc[len(level_data)//2:]['response_time_seconds'].mean()
        queueing_effect = second_half - first_half
        
        ax.text(0.02, 0.98, f'Queueing Effect:\n+{queueing_effect:.1f}s average\nfor later requests', 
                transform=ax.transAxes, fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='#F0F8FF', alpha=0.9, edgecolor='#4682B4'))

plt.suptitle('n8n Queueing Evidence: Response Time Patterns', 
             fontsize=16, fontweight='bold', y=0.95)
plt.tight_layout()

plt.savefig('article_assets/images/n8n_queueing_evidence.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Updated Chart 4: n8n_queueing_evidence.png")
plt.show()

print("\n🎉 All charts updated with consistent blue color scheme!")
print("🎨 Color palette matches the hero chart:")
print("   - Light Blue (#87CEEB) → Steel Blue (#4682B4) → Dodger Blue (#1E90FF) → Navy Blue (#000080)")
print("📊 Charts updated:")
print("   1. n8n_response_distribution.png")
print("   2. n8n_processing_overhead.png") 
print("   3. n8n_throughput_analysis.png")
print("   4. n8n_queueing_evidence.png")
print("✅ All charts now have professional, consistent blue theme!")
