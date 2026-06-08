from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = Path(__file__).with_name("fig2_conceptual_model_clean.pdf")

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

fig, ax = plt.subplots(figsize=(16.8, 8.9))
ax.set_xlim(0, 16.8)
ax.set_ylim(0, 8.9)
ax.axis("off")

colors = {
    "blue": "#DDEAF3",
    "blue_edge": "#2B6F9E",
    "green": "#E4F0E4",
    "green_edge": "#3B7D3A",
    "orange": "#F7E9DC",
    "orange_edge": "#C96C22",
    "purple": "#ECE6F3",
    "purple_edge": "#6B4C8A",
    "line": "#333333",
    "group": "#F7F8FA",
    "group_edge": "#C8CDD3",
}

W, H = 2.28, 0.98

nodes = {
    "channel": (1.35, 7.12, "blue", "blue_edge", "Digital Channel", "App, WeChat mini-program"),
    "customer": (3.95, 7.12, "blue", "blue_edge", "Customer", "Member, commuter, student"),
    "membership": (6.55, 7.12, "blue", "blue_edge", "Membership Account", "Points, coupons, profile"),
    "promotion": (9.15, 7.12, "orange", "orange_edge", "Promotion Campaign", "Coupon, seasonal offer"),
    "order": (2.65, 4.78, "purple", "purple_edge", "Digital Order", "Pickup, delivery order"),
    "orderitem": (2.65, 3.25, "purple", "purple_edge", "Order Item", "Drink line, add-on"),
    "task": (5.55, 4.78, "green", "green_edge", "Fulfilment Task", "Prepare, handover, exception"),
    "store": (8.45, 4.78, "green", "green_edge", "Store", "Self-operated, partner store"),
    "staff": (8.45, 3.25, "green", "green_edge", "Store Staff", "Barista, manager"),
    "delivery": (11.35, 4.78, "orange", "orange_edge", "Delivery Partner", "Courier, delivery platform"),
    "product": (1.35, 1.42, "blue", "blue_edge", "Product", "Coffee drink, light food"),
    "recipe": (3.95, 1.42, "blue", "blue_edge", "Recipe Standard", "Dosage, SOP version"),
    "material": (6.55, 1.42, "orange", "orange_edge", "Raw Material", "Beans, milk, packaging"),
    "supplier": (9.15, 1.42, "orange", "orange_edge", "Supplier", "Bean farm, ingredient vendor"),
    "performance": (12.15, 1.42, "purple", "purple_edge", "Performance Result", "Revenue, margin, complaints"),
}

groups = [
    (0.45, 6.18, 10.35, 1.82, "Demand and customer relationship layer"),
    (1.35, 2.52, 12.05, 3.02, "Transaction and fulfilment layer"),
    (0.45, 0.58, 13.45, 1.74, "Product, resource, and analytics layer"),
]

for x, y, w, h, label in groups:
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.08,rounding_size=0.12",
        linewidth=0.8,
        edgecolor=colors["group_edge"],
        facecolor=colors["group"],
        zorder=0,
    ))
    ax.text(
        x + 0.18,
        y + h - 0.18,
        label,
        fontsize=10.2,
        fontweight="bold",
        va="top",
        color="#222222",
        bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="none", alpha=0.92),
        zorder=6,
    )

for key, (x, y, fill, edge, title, example) in nodes.items():
    ax.add_patch(FancyBboxPatch(
        (x - W / 2, y - H / 2), W, H,
        boxstyle="round,pad=0.08,rounding_size=0.10",
        linewidth=1.15,
        edgecolor=colors[edge],
        facecolor=colors[fill],
        zorder=3,
    ))
    ax.text(x, y + 0.23, title, ha="center", va="center", fontsize=9.4, fontweight="bold", color="#111111", zorder=4)
    ax.text(x, y + 0.02, f"({example})", ha="center", va="center", fontsize=7.0, color="#222222", zorder=4)
    ax.text(x, y - 0.27, "CV / SV / AV / EP", ha="center", va="center", fontsize=6.5, color="#444444", zorder=4)

def anchor(name, side):
    x, y, *_ = nodes[name]
    if side == "r":
        return x + W / 2, y
    if side == "l":
        return x - W / 2, y
    if side == "t":
        return x, y + H / 2
    if side == "b":
        return x, y - H / 2
    return x, y

def arrow(a, aside, b, bside, label, rad=0, dashed=False, text=(0, 0)):
    p1 = anchor(a, aside)
    p2 = anchor(b, bside)
    ax.add_patch(FancyArrowPatch(
        p1, p2,
        arrowstyle="-|>",
        mutation_scale=11,
        linewidth=1.05,
        color=colors["line"],
        linestyle=(0, (4, 3)) if dashed else "solid",
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=3,
        shrinkB=3,
        zorder=2,
    ))
    ax.text(
        (p1[0] + p2[0]) / 2 + text[0],
        (p1[1] + p2[1]) / 2 + text[1],
        label,
        ha="center",
        va="center",
        fontsize=8.0,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.13", facecolor="white", edgecolor="none", alpha=0.95),
        zorder=5,
    )

arrow("channel", "r", "customer", "l", "D1", text=(0, 0.18))
arrow("customer", "r", "membership", "l", "D2", text=(0, 0.18))
arrow("membership", "b", "order", "t", "D3", rad=0.03, text=(-0.28, -0.04))
arrow("membership", "r", "promotion", "l", "D4", text=(0, 0.18))
arrow("promotion", "b", "order", "t", "D5", rad=-0.22, text=(0.25, -0.10))

arrow("order", "b", "orderitem", "t", "F1", text=(-0.22, 0))
arrow("order", "r", "task", "l", "F2", text=(0, 0.18))
arrow("task", "r", "store", "l", "F3", text=(0, 0.18))
arrow("store", "b", "staff", "t", "F4", text=(0.22, 0))
arrow("task", "r", "delivery", "l", "F5", rad=-0.16, text=(0.20, 0.42))

arrow("orderitem", "l", "product", "t", "S1", rad=0.06, text=(-0.23, -0.08))
arrow("product", "r", "recipe", "l", "S2", text=(0, 0.18))
arrow("recipe", "r", "material", "l", "S3", text=(0, 0.18))
arrow("supplier", "l", "material", "r", "S4", text=(0, 0.18))
arrow("material", "t", "store", "b", "S5", rad=-0.13, text=(0.25, 0.05))

arrow("order", "b", "performance", "l", "A1", rad=0.16, dashed=True, text=(0.45, -0.30))
arrow("store", "b", "performance", "t", "A2", rad=-0.18, dashed=True, text=(0.18, -0.03))
arrow("delivery", "b", "performance", "r", "A3", rad=0.12, dashed=True, text=(0.35, 0.08))
arrow("performance", "r", "promotion", "r", "A4", rad=0.30, dashed=True, text=(0.35, 0.35))

legend_x, legend_y = 14.25, 7.10
ax.text(legend_x, legend_y + 0.50, "Object colour legend", ha="left", va="center", fontsize=10.2, fontweight="bold", color="#222222")
for i, (fill, label) in enumerate([
    ("blue", "Demand / customer object"),
    ("purple", "Transaction / analytics object"),
    ("green", "Fulfilment object"),
    ("orange", "Resource / partner object"),
]):
    y = legend_y - i * 0.38
    ax.add_patch(Rectangle((legend_x, y - 0.12), 0.25, 0.18, facecolor=colors[fill], edgecolor=colors[f"{fill}_edge"], linewidth=0.9))
    ax.text(legend_x + 0.35, y - 0.03, label, ha="left", va="center", fontsize=8.8, color="#222222")

ax.text(legend_x, 4.95, "Relationship ID groups", ha="left", va="center", fontsize=10.2, fontweight="bold", color="#222222")
for i, line in enumerate(["D1--D5  Demand", "F1--F5  Fulfilment", "S1--S5  Supply", "A1--A4  Analytics"]):
    ax.text(legend_x, 4.58 - i * 0.32, line, ha="left", va="center", fontsize=8.8, color="#222222")

ax.plot([legend_x, legend_x + 0.55], [3.10, 3.10], color=colors["line"], lw=1.15)
ax.text(legend_x + 0.70, 3.10, "operational relation", fontsize=8.8, va="center", ha="left")
ax.plot([legend_x, legend_x + 0.55], [2.78, 2.78], color=colors["line"], lw=1.15, linestyle=(0, (4, 3)))
ax.text(legend_x + 0.70, 2.78, "feedback relation", fontsize=8.8, va="center", ha="left")

ax.text(
    7.35, 0.28,
    "CV: ClassVariables    SV: SumVariables    AV: AdjVariables    EP: EstParameters",
    ha="center",
    va="center",
    fontsize=9.0,
    color="#333333",
)

fig.tight_layout(pad=0.2)
fig.savefig(OUT, format="pdf", bbox_inches="tight")
print(OUT)
