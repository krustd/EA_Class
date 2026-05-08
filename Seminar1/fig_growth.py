# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib", "seaborn", "numpy"]
# ///
"""Generate growth trend chart for Luckin Coffee (2020–2025)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ---- Seaborn style ----
sns.set_theme(style="whitegrid", context="paper", font_scale=1.1)
plt.rcParams.update(
    {
        "font.family": "serif",
        "text.usetex": False,
    }
)

# ---- Data (approximate from Luckin filings / public reports) ----
years = np.array([2020, 2021, 2022, 2023, 2024, 2025])
stores = np.array([4803, 6024, 8214, 16248, 22340, 31048])  # total stores
revenue = np.array([4.03, 7.97, 13.29, 24.90, 34.46, 49.30])  # RMB billions

# ---- Figure ----
fig, ax1 = plt.subplots(figsize=(6.5, 4.0))

palette = sns.color_palette("muted", 3)
color_stores = palette[0]
color_revenue = palette[2]

# Bars: store count
bars = ax1.bar(
    years - 0.15,
    stores,
    width=0.3,
    color=color_stores,
    alpha=0.85,
    edgecolor="white",
    linewidth=0.6,
    label="Store Count",
    zorder=3,
)
ax1.set_ylabel("Number of Stores", fontsize=12, labelpad=8, color=color_stores)
ax1.tick_params(axis="y", labelcolor=color_stores, labelsize=9)
ax1.set_ylim(0, 38000)

# Annotate bars
for bar, val in zip(bars, stores):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 400,
        f"{val:,}",
        ha="center",
        va="bottom",
        fontsize=7.5,
        color=color_stores,
    )

# Line: revenue
ax2 = ax1.twinx()
(line,) = ax2.plot(
    years,
    revenue,
    color=color_revenue,
    marker="o",
    linewidth=2.2,
    markersize=7,
    markerfacecolor="white",
    markeredgewidth=1.8,
    markeredgecolor=color_revenue,
    label="Total Net Revenue",
    zorder=4,
)
ax2.set_ylabel("Revenue (RMB billions)", fontsize=12, labelpad=10, color=color_revenue)
ax2.tick_params(axis="y", labelcolor=color_revenue, labelsize=9)
ax2.set_ylim(0, 60)

# Annotate line points
for x, y in zip(years, revenue):
    ax2.annotate(
        f"{y:.1f}",
        (x, y),
        textcoords="offset points",
        xytext=(0, 12),
        ha="center",
        fontsize=8.5,
        fontweight="semibold",
        color=color_revenue,
    )

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(
    lines1 + [line],
    labels1 + labels2,
    loc="upper left",
    frameon=True,
    fontsize=9,
    framealpha=0.9,
)

ax1.set_title(
    "Luckin Coffee: Store Count and Revenue Growth (2020–2025)",
    fontsize=14,
    fontweight="bold",
    pad=14,
)
ax1.set_xticks(years)
ax1.set_xticklabels([str(y) for y in years], fontsize=10)
ax1.set_xlim(2019.5, 2025.5)

sns.despine(left=True, bottom=False, right=False)
fig.tight_layout()

fig.savefig("Seminar1/fig_growth.png", dpi=300, bbox_inches="tight")
print("Saved: Seminar1/fig_growth.png")
