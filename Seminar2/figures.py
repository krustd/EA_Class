from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


OUT = Path(__file__).resolve().parent
sns.set_theme(style="whitegrid", context="talk", font="DejaVu Sans")


perspectives = ["Financial", "Customer", "Internal\nProcesses", "Learning\n& Growth"]
capabilities = [
    "Revenue Growth",
    "Cost Discipline",
    "Convenience",
    "Quality Control",
    "Digital Analytics",
    "Innovation",
]
values = np.array(
    [
        [5, 5, 3, 3, 4, 3],
        [4, 2, 5, 5, 4, 4],
        [3, 4, 5, 5, 5, 3],
        [3, 2, 3, 4, 5, 5],
    ]
)
heat_df = pd.DataFrame(values, index=perspectives, columns=capabilities)
fig, ax = plt.subplots(figsize=(12, 6.8))
sns.heatmap(
    heat_df,
    annot=True,
    fmt="d",
    cmap="YlGnBu",
    linewidths=0.8,
    linecolor="white",
    cbar_kws={"label": "Strategic emphasis (1-5)"},
    ax=ax,
)
ax.set_title("Balanced Scorecard Strategic Emphasis Matrix", fontsize=20, weight="bold", pad=16)
ax.set_xlabel("Strategic capability")
ax.set_ylabel("BSC perspective")
plt.tight_layout()
fig.savefig(OUT / "fig_bsc_heatmap.pdf", bbox_inches="tight")
plt.close(fig)


revenue = pd.DataFrame(
    {
        "Source": ["Self-operated stores", "Partnership stores", "Other revenue"],
        "RMB billion": [36.2, 11.6, 1.5],
    }
)
fig, ax = plt.subplots(figsize=(10.5, 6.2))
sns.barplot(
    data=revenue,
    y="Source",
    x="RMB billion",
    hue="Source",
    palette=["#1F77B4", "#2CA02C", "#FFB000"],
    legend=False,
    ax=ax,
)
for container in ax.containers:
    ax.bar_label(container, fmt="%.1f", padding=4, fontsize=12)
ax.set_title("Luckin Coffee FY2025 Revenue Structure", fontsize=20, weight="bold", pad=14)
ax.set_xlabel("Revenue (RMB billion)")
ax.set_ylabel("")
ax.set_xlim(0, 40)
ax.grid(axis="x", alpha=0.25)
plt.tight_layout()
fig.savefig(OUT / "fig_revenue_structure.pdf", bbox_inches="tight")
plt.close(fig)


labels = ["Raw materials", "Rent & utilities", "Labour", "Delivery/logistics", "Marketing", "Technology"]
scores = [5, 4, 4, 4, 5, 3]
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
scores_closed = scores + scores[:1]
angles_closed = angles + angles[:1]
fig = plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)
ax.plot(angles_closed, scores_closed, color="#6A4C93", linewidth=2.5)
ax.fill(angles_closed, scores_closed, color="#6A4C93", alpha=0.22)
ax.set_xticks(angles)
ax.set_xticklabels(labels, fontsize=11)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=10)
ax.set_ylim(0, 5)
ax.set_title("Relative Cost Pressure in Luckin Coffee Model", fontsize=18, weight="bold", pad=24)
ax.grid(alpha=0.35)
plt.tight_layout()
fig.savefig(OUT / "fig_cost_pressure.pdf", bbox_inches="tight")
plt.close(fig)
