import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set random seed for reproducible jitter
np.random.seed(42)

# Read the CSV data
df = pd.read_csv('article_assets/data/n8n_concurrency_test_results.csv')
df['concurrency'] = df['concurrent_requests']

print("=== DEBUGGING CHART DATA ===")
print(f"Total data points: {len(df)}")
print(f"Workload values: {sorted(df['workload_seconds'].unique())}")
print(f"Concurrency levels: {sorted(df['concurrency'].unique())}")

# Check each workload explicitly
for workload in sorted(df['workload_seconds'].unique()):
    subset = df[df['workload_seconds'] == workload]
    print(f"Workload {workload}: {len(subset)} points")

# Create the figure
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

# First, let's try a basic scatter plot to see if all data shows
plt.subplot(1, 2, 1)
scatter = plt.scatter(df['workload_seconds'], df['response_time_seconds'], 
                     c=df['concurrency'], cmap='viridis', alpha=0.7, s=100)
plt.title('Basic Scatter (All Data)')
plt.xlabel('Workload (seconds)')
plt.ylabel('Response time (seconds)')
plt.colorbar(scatter, label='Concurrency')
plt.xticks(range(1, 6))
plt.xlim(0.5, 5.5)

# Now try stripplot
plt.subplot(1, 2, 2)
sns.stripplot(data=df, 
              x='workload_seconds', 
              y='response_time_seconds',
              hue='concurrency',
              size=12,
              alpha=0.8,
              jitter=0.12,
              dodge=False,
              linewidth=2,
              edgecolor='white')

plt.title('Stripplot with Jitter')
plt.xlabel('Workload (seconds)')
plt.ylabel('Response time (seconds)')
plt.xticks(range(1, 6))
plt.xlim(0.5, 5.5)
plt.legend(title='Concurrency', loc='upper left')

plt.tight_layout()
plt.savefig('debug_chart_comparison.png', dpi=200, bbox_inches='tight')
plt.show()

# Print detailed info about 1-second data
one_sec = df[df['workload_seconds'] == 1]
print("\n=== 1-SECOND WORKLOAD DETAILS ===")
for _, row in one_sec.iterrows():
    print(f"Concurrency: {row['concurrency']}, Response: {row['response_time_seconds']:.1f}s, Workload: {row['workload_seconds']}s")
