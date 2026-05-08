# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib", "seaborn", "numpy"]
# ///
"""Generate growth trend chart for Luckin Coffee (2020-2025)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ---- Seaborn style ----
sns.set_theme(style="whitegrid", context="paper", font_scale=1.0)
plt.rcParams.update(
    {
        "font.family": "serif",
        "text.usetex": False,
        "axes.edgecolor": "#444444",
        "axes.labelcolor": "#222222",
        "xtick.color": "#222222",
        "ytick.color": "#222222",
        "grid.color": "#d9d9d9",
        "grid.linewidth": 0.7,
    }
)

# ---- Data (approximate from Luckin filings / public reports) ----
years = np.array([2020, 2021, 2022, 2023, 2024, 2025])
stores = np.array([4803, 6024, 8214, 16248, 22340, 31048])  # total stores
revenue = np.array([4.03, 7.97, 13.29, 24.90, 34.46, 49.30])  # RMB billions

# ---- Figure ----
fig, (ax_stores, ax_revenue) = plt.subplots(
    2,
    1,
    figsize=(6.6, 4.6),
    sharex=True,
    constrained_layout=True,
    gridspec_kw={"height_ratios": [1, 1], "hspace": 0.18},
)

store_color = "#3f6fb5"
revenue_color = "#2e8b57"

ax_stores.bar(
    years,
    stores / 1000,
    width=0.48,
    color=store_color,
    alpha=0.82,
    edgecolor="#ffffff",
    linewidth=0.6,
)
ax_stores.set_ylabel("Stores\n(thousand)", fontsize=9)
ax_stores.set_ylim(0, 35)
ax_stores.set_yticks([0, 10, 20, 30])
ax_stores.text(
    0.01,
    0.9,
    "Store count",
    transform=ax_stores.transAxes,
    fontsize=9.5,
    fontweight="bold",
    color=store_color,
)

ax_revenue.plot(
    years,
    revenue,
    color=revenue_color,
    marker="o",
    linewidth=2.0,
    markersize=4.8,
)
ax_revenue.set_ylabel("Revenue\n(RMB bn)", fontsize=9)
ax_revenue.set_ylim(0, 55)
ax_revenue.set_yticks([0, 15, 30, 45])
ax_revenue.text(
    0.01,
    0.9,
    "Total net revenue",
    transform=ax_revenue.transAxes,
    fontsize=9.5,
    fontweight="bold",
    color=revenue_color,
)

# Label only the endpoints to keep the figure readable in the report.
ax_stores.annotate(
    f"{stores[0] / 1000:.1f}k",
    (years[0], stores[0] / 1000),
    textcoords="offset points",
    xytext=(0, 6),
    ha="center",
    fontsize=8,
    color="#333333",
)
ax_stores.annotate(
    f"{stores[-1] / 1000:.1f}k",
    (years[-1], stores[-1] / 1000),
    textcoords="offset points",
    xytext=(0, 6),
    ha="center",
    fontsize=8,
    color="#333333",
)
ax_revenue.annotate(
    f"{revenue[0]:.1f}",
    (years[0], revenue[0]),
    textcoords="offset points",
    xytext=(0, 7),
    ha="center",
    fontsize=8,
    color="#333333",
)
ax_revenue.annotate(
    f"{revenue[-1]:.1f}",
    (years[-1], revenue[-1]),
    textcoords="offset points",
    xytext=(0, 7),
    ha="center",
    fontsize=8,
    color="#333333",
)

for ax in (ax_stores, ax_revenue):
    ax.set_xlim(2019.55, 2025.45)
    ax.grid(True, axis="y")
    ax.grid(False, axis="x")
    ax.tick_params(axis="both", labelsize=8.5)

ax_revenue.set_xticks(years)
ax_revenue.set_xticklabels([str(y) for y in years], fontsize=8.5)

fig.suptitle(
    "Luckin Coffee: Store Count and Revenue Growth, 2020-2025",
    fontsize=11,
    fontweight="bold",
)

sns.despine()

fig.savefig("Seminar1/fig_growth.png", dpi=300, bbox_inches="tight")
print("Saved: Seminar1/fig_growth.png")
