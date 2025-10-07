import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set random seed for reproducible jitter
np.random.seed(42)

# Read the CSV data using the correct file
df = pd.read_csv('article_assets/data/n8n_concurrency_test_results.csv')

# Convert response time to milliseconds and rename columns for clarity
df['response_time_ms'] = df['response_time_seconds'] * 1000
df['concurrency'] = df['concurrent_requests']

# Create the figure and axis
plt.figure(figsize=(12, 8))

# Set seaborn style for better aesthetics
sns.set_style("whitegrid")

# Create the scatter plot with jitter using seaborn stripplot
ax = sns.stripplot(data=df, 
                   x='workload_seconds', 
                   y='response_time_ms',
                   hue='concurrency',
                   size=14,  # Larger dots
                   alpha=0.8,
                   jitter=0.12,  # Strong jitter for clear separation
                   dodge=False,
                   linewidth=2.5,  # White border width
                   edgecolor='white')  # White border

# Customize the plot - ONLY subtitle, no main title
plt.title('Response Times vs Workload Under Load', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Workload (seconds)', fontsize=14, fontweight='bold')
plt.ylabel('Response Time (ms)', fontsize=14, fontweight='bold')

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

# Set axis limits with some padding
plt.xlim(0.5, 5.5)
plt.ylim(0, df['response_time_ms'].max() * 1.1)

# Improve tick labels
plt.xticks(range(1, 6), fontsize=12)
plt.yticks(fontsize=12)

# NO CALLOUTS/ANNOTATIONS - removed completely

# Tight layout for better spacing
plt.tight_layout()

# Save the enhanced chart
plt.savefig('article_assets/images/n8n_hero_chart_clear.png', 
           dpi=300, 
           bbox_inches='tight',
           facecolor='white',
           edgecolor='none')

plt.show()

print("✅ Hero chart updated successfully!")
print("🚫 Removed all callouts/annotations")
print("📍 Kept all other enhancements:")
print("   - No main title (only subtitle)")
print("   - Strong horizontal jitter for data separation") 
print("   - Legend in lower-right corner")
print("   - Large dots with white borders")
print("   - Professional styling")
print("   - Clean, uncluttered appearance")
