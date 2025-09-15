import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from matplotlib.ticker import MaxNLocator, MultipleLocator, PercentFormatter
import calendar
import matplotlib.patches as patches
import numpy as np

# === Load CSV with correct delimiter and decimal ===
df = pd.read_csv("Oee_evolution.csv", sep=";", decimal=",",
                 usecols=["Month Number", "Month Name", "Week Number", "OEE"])

# Rename columns for easier handling
df = df.rename(columns={
    "Month Number": "Month",
    "Month Name": "MonthName",
    "Week Number": "Week"
})

# Drop rows without OEE values
df = df.dropna(subset=["OEE"])

# Ensure numeric types
df["Month"] = pd.to_numeric(df["Month"], errors="coerce").astype(int)
df["Week"] = pd.to_numeric(df["Week"], errors="coerce").astype(int)
df["OEE"] = pd.to_numeric(df["OEE"], errors="coerce")

# === Convert to percentage ===
df["OEE"] = df["OEE"] * 100

# === Set goal for OEE (in %) ===
goal = 0.40 * 100  # 40%

# Assign colors based on OEE vs goal
colors = ["green" if x >= goal else "red" for x in df["OEE"]]

# === Plot setup ===
sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(25, 12))
bar_width = 0.2

# Bar chart
bars = ax1.bar(df["Week"], df["OEE"], width=bar_width, color=colors, edgecolor='black')

# Trendline calculation
x = df["Week"].values
y = df["OEE"].values
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
ax1.plot(x, p(x), color="black", linestyle="-", linewidth=2, label="Trendline")

# Goal line
ax1.axhline(goal, color="green", linestyle="--", linewidth=2, label=f"Goal: {goal:.1f}%")

# Event lines
ax1.axvline(x=9.5, color="darkgreen", linestyle="-", linewidth=2, zorder=0)
ax1.text(9.65, ax1.get_ylim()[1]*0.98, "Start of DK Meetings",
         rotation=90, va='top', color="darkgreen", fontsize=12)
ax1.axvline(x=10.5, color="darkblue", linestyle="-", linewidth=2, zorder=0)
ax1.text(10.65, ax1.get_ylim()[1]*0.98, "Start of Standard Operation",
         rotation=90, va='top', color="darkblue", fontsize=12)
ax1.axvline(x=24, color="red", linestyle="-", linewidth=2, zorder=0)
ax1.text(24.5, ax1.get_ylim()[1]*0.96, "New Product Introduced",
         rotation=90, va='top', color="red", fontsize=12)

# Baseline and Improved OEE
baseline_oee = df.loc[df["Week"].between(5, 9), "OEE"].mean()
improved_oee = df.loc[df["Month"] == 7, "OEE"].mean()

ax1.hlines(
    y=baseline_oee, xmin=5, xmax=9,
    colors="darkred", linestyles="-", linewidth=2,
    label=f"Baseline OEE: {baseline_oee:.1f}%"
)

ax1.hlines(
    y=improved_oee, xmin=28, xmax=31,
    colors="darkgreen", linestyles="-", linewidth=2,
    label=f"Improved OEE (July): {improved_oee:.1f}%"
)

# Axis labels
ax1.set_ylabel("OEE (%)", fontsize=12, fontweight='bold')
ax1.set_xlabel("Week", fontsize=12, fontweight='bold')
ax1.set_xticks(df["Week"])
ax1.set_xticklabels(df["Week"].astype(int))
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax1.xaxis.set_major_locator(MultipleLocator(1))
ax1.yaxis.set_major_formatter(PercentFormatter())  # show % on y-axis
ax1.set_xlim(3, 32)

# Annotate bars with %
for p in bars:
    ax1.annotate(f'{p.get_height():.1f}%', 
                 (p.get_x() + p.get_width() / 2., p.get_height()/2.),
                 ha='center', va='bottom', fontsize=9, color="black", xytext=(0, 3),
                 textcoords="offset points",
                 bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))

# Draw month boxes
ymin, ymax = ax1.get_ylim()
months = df["Month"].unique()
months.sort()
for m in months:
    weeks_in_month = df.loc[df["Month"] == m, "Week"]
    if not weeks_in_month.empty:
        start_week = weeks_in_month.min() - bar_width/2
        end_week = weeks_in_month.max() + bar_width/2
        width = end_week - start_week
        rect = patches.Rectangle((start_week, ymin), width, 5,  # adjusted height
                                 linewidth=2, edgecolor='black', facecolor='lightgray',
                                 alpha=0.8, zorder=1)
        ax1.add_patch(rect)
        ax1.text((start_week + end_week)/2, ymin + 2.5, calendar.month_name[m],
                 ha='center', va='center', fontsize=10, fontweight='bold', zorder=1)

plt.subplots_adjust(bottom=0.25)
ax1.legend(loc="best")

# Title and save
title = 'Evolution of OEE along the weeks'
filename = title.replace(" ", "_").replace("/", "_") + ".png"
folder = '../Pictures/'
os.makedirs(folder, exist_ok=True)
plt.savefig(folder+filename, dpi=300)
plt.show()

