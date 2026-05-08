# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib", "seaborn", "numpy"]
# ///
"""Generate stakeholder map for Luckin Coffee."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_theme(style="white", context="paper", font_scale=1.05)
plt.rcParams.update(
    {
        "font.family": "serif",
        "text.usetex": False,
    }
)

fig, ax = plt.subplots(figsize=(7.0, 5.5))
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_aspect("equal")
ax.axis("off")

# ---- Concentric rings ----
rings = [1.5, 3.0, 4.5]
ring_colors = ["#2a5c8a", "#4a8ab5", "#a8cce0"]
ring_labels = ["Core", "Strategic", "Peripheral"]

for r, c, lbl in zip(rings, ring_colors, ring_labels):
    circle = plt.Circle(
        (0, 0), r, fill=True, facecolor=c, alpha=0.12, edgecolor=c, linewidth=1.3
    )
    ax.add_patch(circle)
    ax.text(
        0,
        -r - 0.22,
        lbl,
        ha="center",
        va="top",
        fontsize=9,
        fontstyle="italic",
        color=c,
    )

# ---- Stakeholder placements (angle in radians, radius, label) ----
stakeholders = [
    # Core (r < 1.5)
    (np.radians(30), 1.0, "Customers", "#1a3a5c"),
    (np.radians(150), 1.0, "Employees", "#1a3a5c"),
    (np.radians(270), 1.0, "Store Operators", "#1a3a5c"),
    # Strategic (1.5 < r < 3.0)
    (np.radians(10), 2.2, "Suppliers", "#2a5078"),
    (np.radians(70), 2.2, "Logistics Partners", "#2a5078"),
    (np.radians(130), 2.2, "Tech Providers", "#2a5078"),
    (np.radians(190), 2.2, "Delivery Platforms", "#2a5078"),
    (np.radians(250), 2.2, "Payment Platforms", "#2a5078"),
    (np.radians(310), 2.2, "Landlords", "#2a5078"),
    # Peripheral (3.0 < r < 4.5)
    (np.radians(30), 3.8, "Investors", "#4a6a88"),
    (np.radians(110), 3.8, "Regulators (SEC)", "#4a6a88"),
    (np.radians(200), 3.8, "Local Communities", "#4a6a88"),
    (np.radians(290), 3.8, "Corporate Clients", "#4a6a88"),
]

for angle, radius, label, color in stakeholders:
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    # Circle marker
    ax.plot(
        x,
        y,
        "o",
        color=color,
        markersize=9,
        markeredgecolor="white",
        markeredgewidth=1.2,
        zorder=5,
    )
    # Label with offset
    offset_r = 0.35
    tx = (radius + offset_r) * np.cos(angle)
    ty = (radius + offset_r) * np.sin(angle)
    ha = "center"
    if angle < np.radians(10) or angle > np.radians(350):
        ha = "left"
    elif np.radians(170) < angle < np.radians(190):
        ha = "right"
    ax.text(
        tx,
        ty,
        label,
        ha=ha,
        va="center",
        fontsize=8.5,
        fontweight="medium",
        color=color,
        zorder=5,
    )

# Centre label
ax.text(
    0,
    0,
    "Luckin\nCoffee",
    ha="center",
    va="center",
    fontsize=13,
    fontweight="bold",
    color="#0d2b45",
)

ax.set_title(
    "Stakeholder Map: Luckin Coffee Ecosystem", fontsize=14, fontweight="bold", pad=12
)

fig.tight_layout()
fig.savefig("Seminar1/fig_stakeholders.png", dpi=300, bbox_inches="tight")
print("Saved: Seminar1/fig_stakeholders.png")
