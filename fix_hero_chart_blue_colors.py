import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set random seed for reproducible jitter
np.random.seed(42)

# Read the CSV data
df = pd.read_csv('article_assets/data/n8n_concurrency_test_results.csv')
df['concurrency'] = df['concurrent_requests']

print("=== DATA VERIFICATION ===")
print(f"Total data points: {len(df)}")
print(f"Workload values: {sorted(df['workload_seconds'].unique())}")
print(f"Concurrency levels: {sorted(df['concurrency'].unique())}")

# Verify 1-second data is included
one_sec = df[df['workload_seconds'] == 1]
print(f"\n1-second workload: {len(one_sec)} points")
print("Concurrency distribution for 1s workload:")
print(one_sec['concurrency'].value_counts().sort_index())

# Create the figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Set seaborn style
sns.set_style("whitegrid")

# Define blue color scheme - from light blue to navy
blue_colors = [
    '#87CEEB',  # Light blue (5 requests)
    '#4682B4',  # Steel blue (10 requests)  
    '#1E90FF',  # Dodger blue (20 requests)
    '#000080'   # Navy blue (30 requests)
]

# Create color mapping for concurrency levels
concurrency_levels = sorted(df['concurrency'].unique())
color_map = dict(zip(concurrency_levels, blue_colors))

# Add manual jitter to workload values
jitter_strength = 0.12
df_plot = df.copy()
df_plot['workload_jittered'] = df_plot['workload_seconds'] + np.random.uniform(-jitter_strength, jitter_strength, len(df_plot))

# Plot each concurrency level separately to ensure visibility
for conc_level in concurrency_levels:
    subset = df_plot[df_plot['concurrency'] == conc_level]
    plt.scatter(subset['workload_jittered'], subset['response_time_seconds'],
                c=color_map[conc_level], 
                label=f'{conc_level}',
                s=140,  # Large dots
                alpha=0.8,
                edgecolors='white',
                linewidth=2.5)
    
    print(f"Plotted {len(subset)} points for concurrency {conc_level} in {color_map[conc_level]}")

# Customize the plot
plt.title('Response time vs Workload', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Workload (seconds)', fontsize=14, fontweight='bold')
plt.ylabel('Response time (seconds)', fontsize=14, fontweight='bold')

# Customize the legend - position in lower-right
legend = plt.legend(title='Concurrency Level', 
                   loc='lower right',
                   frameon=True,
                   fancybox=True,
                   shadow=True,
                   title_fontsize=12,
                   fontsize=11)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_alpha(0.95)

# Customize grid
plt.grid(True, linestyle=':', alpha=0.6)

# Set axis limits - make sure all data is visible
plt.xlim(0.5, 5.5)
plt.ylim(0, df['response_time_seconds'].max() * 1.1)

# Set explicit ticks to show all workload values
plt.xticks(range(1, 6), fontsize=12)
plt.yticks(fontsize=12)

# Tight layout
plt.tight_layout()

# Save the chart
plt.savefig('article_assets/images/n8n_hero_chart_clear.png', 
           dpi=300, 
           bbox_inches='tight',
           facecolor='white',
           edgecolor='none')

plt.show()

print("\n✅ Hero chart updated with blue color scheme!")
print("🎨 Color scheme changed to shades of blue:")
print("   - Concurrency 5: Light Blue (#87CEEB)")
print("   - Concurrency 10: Steel Blue (#4682B4)")
print("   - Concurrency 20: Dodger Blue (#1E90FF)")
print("   - Concurrency 30: Navy Blue (#000080)")
print("📍 All other features kept unchanged:")
print(f"   - All {len(df)} data points included")
print(f"   - 1-second workload: {len(one_sec)} points verified")
print("   - Manual jitter, legend position, styling all preserved")
