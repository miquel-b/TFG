import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import MultipleLocator
import calendar
import matplotlib.patches as patches

df=pd.read_excel("Cleaning_Time_Data.xlsx",usecols=["Year","Month", "Week", "Time (h)"])
df["Time (h)"] = df["Time (h)"].astype(str).str.replace(",", ".").astype(float)
df = df.dropna(subset=["Year", "Month", "Week","Time (h)"])
df["Month"] = df["Month"].astype(int)
df["Year"] = df["Year"].astype(int)
df["Week"] = df["Week"].astype(int)

print(df)

goal=2+15/60
# Assign colors based on average time
colors = ["green" if x <= goal else "red" for x in df["Time (h)"]]

# Seaborn theme
sns.set_theme(style="whitegrid")

# Create plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Bar plot with seaborn colors
bar_width=0.2
barplot=ax1.bar(df["Week"], df["Time (h)"], width=bar_width, color=colors, edgecolor='black')
# Line connecting the monthly averages
lineplot = ax1.plot(
    df["Week"], 
    df["Time (h)"],
    color="black",      # line color
    linestyle="-",      # dashed line
    marker="o",          # show points
    linewidth=1,
)

# Add horizontal goal line at 2.33 h
ax1.axhline(goal, color="green", linestyle="--", linewidth=2, label=f"Goal: {goal} h")

# Add vertical dashed line at month 2 for start of Dk meetings
ax1.axvline(x=9.5, color="darkgreen", linestyle="-", linewidth=2,zorder=0)  # 2 corresponds to first bar
ax1.text(9.65, ax1.get_ylim()[1]*0.98, "Start of DK Meetings", rotation=90,verticalalignment='top', color="darkgreen", fontsize=12,zorder=2)



# Add vertical dashed line at month 2 for start of Standard Operation
ax1.axvline(x=10.5, color="darkblue", linestyle="-", linewidth=2,zorder=0)  # 2 corresponds to first bar
ax1.text(10.65, ax1.get_ylim()[1]*0.98, "Start of Standard Operation", rotation=90,verticalalignment='top', color="darkblue", fontsize=12,zorder=2)


ax1.axvline(x=24, color="red", linestyle="-", linewidth=2,zorder=0)  # 2 corresponds to first bar
ax1.text(24.5, ax1.get_ylim()[1]*0.96, "New Product Introduced", rotation=90,
         verticalalignment='top', color="red", fontsize=12)


ax1.set_ylabel("Total Time of machine inactivity when Cleaning(h)", fontsize=12,fontweight='bold')
ax1.set_xlabel("Week", fontsize=12,fontweight='bold')
ax1.set_xticks(df["Week"])
ax1.set_xticklabels(df["Week"].astype(int))  # optional
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax1.xaxis.set_major_locator(MultipleLocator(1))
# Set y-axis major ticks every 0.5
ax1.yaxis.set_major_locator(MultipleLocator(0.5))
ax1.set_xlim(8,32)
# Add 80% Pareto line
#ax1.axhline(80, color="black", linestyle="--", linewidth=1.5, label="80% Threshold")

# Annotate bars
for p in barplot:
    ax1.annotate(
        f'{p.get_height():.1f}h', 
        (p.get_x() + p.get_width() / 2., p.get_height()/2.),
        ha='center', va='bottom', fontsize=9, color="black", xytext=(0, 3),
        textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")
    )

# Make sure bar_width matches your bars
bar_width = 0.2

# Adjust y-axis to leave space at the bottom for month boxes
ymin, ymax = ax1.get_ylim()

# Draw month boxes
months = df["Month"].unique()
months.sort()

for m in months:
    weeks_in_month = df.loc[df["Month"] == m, "Week"]
    if not weeks_in_month.empty:
        start_week = weeks_in_month.min() - bar_width/2
        end_week = weeks_in_month.max() + bar_width/2
        width = end_week - start_week

        # Rectangle for the month
        rect = patches.Rectangle(
            (start_week, ymin),  # x, y position below bars
            width,
            0.5,                       # height of rectangle
            linewidth=2,
            edgecolor='black',
            facecolor='lightgray',
            alpha=0.8,
            zorder=1                   # before bars
        )
        ax1.add_patch(rect)

        # Month label centered
        ax1.text(
            (start_week + end_week)/2,
            ymin + 0.25,
            calendar.month_name[m],
            ha='center', va='center', fontsize=10, fontweight='bold',zorder=1
        )
# Adjust bottom margin to fit month boxes
plt.subplots_adjust(bottom=0.25)

# Titles and legend
title='Evolution of cleaning time along the weeks'
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
