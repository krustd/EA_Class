# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib", "seaborn", "numpy"]
# ///
"""Generate revenue structure chart for Luckin Coffee FY2025."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ---- Seaborn style ----
sns.set_theme(style="whitegrid", context="paper", font_scale=1.15)
plt.rcParams.update(
    {
        "font.family": "serif",
        "text.usetex": False,
    }
)

# ---- Data ----
categories = ["Self-Operated\nStores", "Partnership\nStores"]
revenue = [36.2, 11.6]  # RMB billions
percent = [73.5, 26.5]

colors = sns.color_palette("muted", 2)

# ---- Figure ----
fig, ax = plt.subplots(figsize=(5.5, 4.2))

bars = ax.bar(
    categories, revenue, color=colors, width=0.45, edgecolor="white", linewidth=0.8
)

# Annotate bars with value and percentage
for bar, val, pct in zip(bars, revenue, percent):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.6,
        f"RMB {val:.1f} bn\n({pct:.1f}\\%)",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold",
        color="#333333",
    )

ax.set_ylabel("Revenue (RMB billions)", fontsize=12, labelpad=10)
ax.set_title(
    "Luckin Coffee FY2025 Revenue by Store Type", fontsize=14, fontweight="bold", pad=16
)
ax.set_ylim(0, 44)
ax.tick_params(axis="x", labelsize=11)
ax.tick_params(axis="y", labelsize=10)

# Subtle total annotation
ax.text(
    0.98,
    0.93,
    "Total: RMB 49.3 bn",
    transform=ax.transAxes,
    ha="right",
    fontsize=10,
    bbox=dict(
        boxstyle="round,pad=0.3", facecolor="#f5f5f5", edgecolor="#cccccc", alpha=0.8
    ),
)

sns.despine(left=True, bottom=False)
fig.tight_layout()

fig.savefig("Seminar1/fig_revenue.png", dpi=300, bbox_inches="tight")
print("Saved: Seminar1/fig_revenue.png")
