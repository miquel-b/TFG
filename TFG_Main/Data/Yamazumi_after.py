
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV (adjust sep=';' because your file uses semicolons)
df = pd.read_csv("Line_Tasks_After.csv", sep=';', decimal=',')
# Strip spaces from operator columns just in case
df['OP alpha'] = df['OP alpha'].str.strip()
df['OP beta'] = df['OP beta'].str.strip()
# Convert numeric columns that may be strings to floats
numeric_cols = ['Time (s)', 'Frequency (1/s)', 'Unitary Time (s)',
                'Time dedication by alpha', 'uts / h alpha',
                'Time dedication by beta', 'uts / h beta']

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
# Prepare data for plotting
# We'll create a row for each operator-task pair
tasks_plot = []

for _, row in df.iterrows():
    # Alpha contribution
    if row['Time dedication by alpha'] > 0:
        tasks_plot.append({
            'Operator': row['OP alpha'].strip(),
            'Task': row['Task'],
            'Time': row['Time dedication by alpha'],
            'VA/MUDA': row['VA/MUDA']
        })
        
    # Beta contribution
    if row['Time dedication by beta'] > 0:
        tasks_plot.append({
            'Operator': row['OP beta'].strip(),
            'Task': row['Task'],
            'Time': row['Time dedication by beta'],
            'VA/MUDA': row['VA/MUDA']
        })

plot_df = pd.DataFrame(tasks_plot)

# Sort tasks by time for stacking order (optional)
plot_df = plot_df.sort_values(by=['Operator', 'Time'], ascending=[True, False])

# Plot Yamazumi
fig, ax = plt.subplots(figsize=(14, 8))

colors = {'VA': 'green', 'MUDA': 'red'}

for operator, group in plot_df.groupby('Operator'):
    bottom = 0
    for _, task in group.iterrows():
        ax.bar(
            operator,
            task['Time'],
            bottom=bottom,
            color=colors[task['VA/MUDA']],
            edgecolor='black',
            linewidth=0.8
        )
        bottom += task['Time']

# Optional: add Takt Time line (adjust as needed)
TaktTime = 2.8
ax.axhline(TaktTime, color="blue", linestyle="--", linewidth=2, label=f"Takt Time: {TaktTime} s")

# Labels & formatting
ax.set_title('Yamazumi Chart (After Kaizen)', fontsize=16, fontweight='bold')
ax.set_ylabel('Unitary Task Time (s)', fontsize=14)
ax.set_xlabel('Operator', fontsize=14)
ax.legend(handles=[plt.Rectangle((0,0),1,1,color='green'),
                   plt.Rectangle((0,0),1,1,color='red'),
                   plt.Line2D([0],[0],color='blue',linestyle='--')],
          labels=['VA','MUDA',f'Takt Time: {TaktTime} s'],
          title='Legend')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("../Pictures/yamazumi_chart_after_kaizen.png", dpi=300)
plt.show()

