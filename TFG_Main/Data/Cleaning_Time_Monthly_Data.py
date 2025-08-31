import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import MultipleLocator

df=pd.read_excel("Cleaning_Time_Data.xlsx",usecols=["Year","Month", "Week", "Time (h)"])
df["Time (h)"] = df["Time (h)"].astype(str).str.replace(",", ".").astype(float)
df["Month"] = df["Month"].dropna().astype(int)
df["Year"] = df["Year"].dropna().astype(int)
df["Week"] = df["Week"].dropna().astype(int)
print(df)

goal=2.33

# Aggregate weekly data to monthly average
monthly_avg = df.groupby("Month")["Time (h)"].mean().reset_index()
# Assign colors based on average time
colors = ["green" if x <= goal else "red" for x in monthly_avg["Time (h)"]]

# Seaborn theme
sns.set_theme(style="whitegrid")

# Create plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Bar plot with seaborn colors
bar_width=0.2
barplot = sns.barplot(
    x="Month", y="Time (h)", data=monthly_avg,
    palette=colors, edgecolor='black',width=bar_width, ax=ax1
)

'''
# Line plot for cumulative percentage
sns.lineplot(
    x="Activity type", y="Cumulative %", data=df,
    color="black", marker="o", linewidth=2, ax=ax1
)
    '''

'''
# Line connecting the monthly averages
lineplot = sns.lineplot(
    x="Month", 
    y="Time (h)",
    data=monthly_avg,
    color="black",      # line color
    linestyle="--",      # dashed line
    marker="o",          # show points
    linewidth=2,
    ax=ax1,
    label="Monthly Average Trend"
)
'''

# Add horizontal goal line at 2.33 h
ax1.axhline(goal, color="green", linestyle="--", linewidth=2, label=f"Goal: {goal} h")
# Add vertical dashed line at month 2 for start of Standard Operation
ax1.axvline(x=1.5, color="black", linestyle="-", linewidth=2)  # 2 corresponds to first bar
ax1.text(1.35, ax1.get_ylim()[1]*0.95, "Start of Standard Operation", rotation=90,
         verticalalignment='top', color="black", fontsize=12)
ax1.set_ylabel("Total Time for Cleaning (h)", fontsize=12,fontweight='bold')
ax1.set_xlabel("Month", fontsize=12,fontweight='bold')
ax1.set_xticks(monthly_avg["Month"])
ax1.set_xticklabels(monthly_avg["Month"].astype(int))  # optional
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
# Set y-axis major ticks every 0.5
ax1.yaxis.set_major_locator(MultipleLocator(0.5))
ax1.set_xlim(0,8)
# Add 80% Pareto line
#ax1.axhline(80, color="black", linestyle="--", linewidth=1.5, label="80% Threshold")

# Annotate bars
for p in barplot.patches:
    ax1.annotate(
        f'{p.get_height():.1f}h', 
        (p.get_x() + p.get_width() / 2., p.get_height()/2.),
        ha='center', va='bottom', fontsize=9, color="black", xytext=(0, 3),
        textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")
    )


# Titles and legend
title='Evolution of cleaning time along the months'
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
