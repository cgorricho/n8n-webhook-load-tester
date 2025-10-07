import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set random seed for reproducible jitter
np.random.seed(42)

# Read the CSV data using the correct file
df = pd.read_csv('article_assets/data/n8n_concurrency_test_results.csv')

# Keep response time in seconds (no conversion to milliseconds)
df['concurrency'] = df['concurrent_requests']

print(f"Data loaded: {len(df)} data points")
print(f"Workload values: {sorted(df['workload_seconds'].unique())}")
print(f"Concurrency levels: {sorted(df['concurrency'].unique())}")

# Create the figure and axis
plt.figure(figsize=(12, 8))

# Set seaborn style for better aesthetics
sns.set_style("whitegrid")

# Create the scatter plot with jitter using seaborn stripplot
ax = sns.stripplot(data=df, 
                   x='workload_seconds', 
                   y='response_time_seconds',  # Keep in seconds
                   hue='concurrency',
                   size=14,  # Larger dots
                   alpha=0.8,
                   jitter=0.12,  # Strong jitter for clear separation
                   dodge=False,
                   linewidth=2.5,  # White border width
                   edgecolor='white')  # White border

# Customize the plot - corrected title
plt.title('Response time vs Workload', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Workload (seconds)', fontsize=14, fontweight='bold')
plt.ylabel('Response time (seconds)', fontsize=14, fontweight='bold')  # Both axes in seconds

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

# Set axis limits with some padding - ensure all workload values are visible
plt.xlim(0.5, 5.5)
plt.ylim(0, df['response_time_seconds'].max() * 1.1)

# Improve tick labels - ensure 1-5 seconds are all shown
plt.xticks(range(1, 6), fontsize=12)
plt.yticks(fontsize=12)

# NO CALLOUTS/ANNOTATIONS - clean design

# Tight layout for better spacing
plt.tight_layout()

# Save the enhanced chart
plt.savefig('article_assets/images/n8n_hero_chart_clear.png', 
           dpi=300, 
           bbox_inches='tight',
           facecolor='white',
           edgecolor='none')

plt.show()

print("✅ Hero chart corrected successfully!")
print("🔧 Fixed issues:")
print("   - Restored all 1-second workload data points") 
print("   - Changed title to: 'Response time vs Workload'")
print("   - Both axes now use seconds as units")
print("📊 Data verification:")
print(f"   - Total data points: {len(df)}")
print(f"   - Workload range: {df['workload_seconds'].min()}-{df['workload_seconds'].max()} seconds")
print(f"   - Response time range: {df['response_time_seconds'].min():.1f}-{df['response_time_seconds'].max():.1f} seconds")
