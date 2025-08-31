import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import pandas as pd
import seaborn as sns
import os

data={
        "Activity type": ["Complete Cleaning", "Format Changeover", "Batch Change", "Others"],
        "Production Times (h)": [2.3255*24,0.4691*24,0.2653*24,0.2369*24]}

df=pd.DataFrame(data)

# Sort by Production Times
df = df.sort_values(by="Production Times (h)", ascending=False).reset_index(drop=True)
#Percentatge
df["Total Time %"] = df["Production Times (h)"] / df["Production Times (h)"].sum() * 100
# Cumulative %
df["Cumulative %"] = df["Production Times (h)"].cumsum() / df["Production Times (h)"].sum() * 100
print(df)
# Assign colors using list comprehension
colors = ["green" if x <= 80 else "red" for x in df["Cumulative %"]]
# Seaborn theme
sns.set_theme(style="whitegrid")

# Create plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Bar plot with seaborn colors
bar_width=0.2
barplot = sns.barplot(
    x="Activity type", y="Total Time %", data=df,
    palette=colors, edgecolor='black',width=bar_width, ax=ax1
)
# Line plot for cumulative percentage
sns.lineplot(
    x="Activity type", y="Cumulative %", data=df,
    color="black", marker="o", linewidth=2, ax=ax1
)
ax1.yaxis.set_major_formatter(PercentFormatter())
ax1.set_ylabel("% of Total Availability lost Time", fontsize=12,fontweight='bold')
ax1.set_xlabel("Activity Type", fontsize=12,fontweight='bold')
ax1.tick_params(axis='x', rotation=0)


# Add 80% Pareto line
ax1.axhline(80, color="black", linestyle="--", linewidth=1.5, label="80% Threshold")

# Annotate bars
for p in barplot.patches:
    ax1.annotate(
        f'{p.get_height():.1f}%', 
        (p.get_x() + p.get_width() / 2., p.get_height()/2.),
        ha='center', va='bottom', fontsize=9, color="black", xytext=(0, 3),
        textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")
    )

# Titles and legend
title='Pareto Chart of Available Time Losses'
#plt.title(title, fontsize=14, fontweight="bold")
ax1.legend(loc="best")

plt.tight_layout()
# Make a valid filename by replacing spaces and removing invalid characters
filename = title.replace(" ", "_").replace("/", "_") + ".png"
# Save as PNG
folder = '../Pictures/'
os.makedirs(folder, exist_ok=True)  # creates the folder if it doesn't exist
plt.savefig(folder+filename, dpi=300) 
plt.show()
