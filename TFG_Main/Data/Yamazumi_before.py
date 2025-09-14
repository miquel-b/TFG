
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV (adjust sep=';' because your file uses semicolons)
df = pd.read_csv("Line_Tasks_Before.csv", sep=';')

# Calculate unitary time
df['Unitary Time'] = df['Time (s)'] * df['Frequency (1/s)']

# Sort data so stacking order is consistent
df = df.sort_values(by=['Operator', 'MUDA/VA', 'Unitary Time'], ascending=[True, True, False])

TaktTime = 2.8

# Plot
fig, ax = plt.subplots(figsize=(14, 8))

# Assign colors by MUDA/VA
colors = {'VA': 'green', 'MUDA': 'red'}

# Group by operator
for i, (operator, group) in enumerate(df.groupby('Operator')):
    bottom = 0
    for _, row in group.iterrows():
        ax.bar(
            operator,
            row['Unitary Time'],
            bottom=bottom,
            color=colors[row['MUDA/VA']],
            edgecolor='black',       # Border for each task
            linewidth=0.8
        )
        bottom += row['Unitary Time']

# Add Takt Time line
ax.axhline(TaktTime, color="blue", linestyle="--", linewidth=2, label=f"Takt Time: {TaktTime} s")

# Labels & Formatting
ax.set_title('Yamazumi Chart (Before Kaizen)', fontsize=16, fontweight='bold')
ax.set_ylabel('Task Unitary Time (s)', fontsize=14)
ax.set_xlabel('Operator', fontsize=14)
ax.legend(handles=[plt.Rectangle((0,0),1,1,color='green'),
                   plt.Rectangle((0,0),1,1,color='red'),
                   plt.Line2D([0],[0],color='blue',linestyle='--')],
          labels=['VA','MUDA',f'Takt Time: {TaktTime} s'],
          title='Legend')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("../Pictures/yamazumi_chart_before_kaizen.png", dpi=300)
plt.show()

