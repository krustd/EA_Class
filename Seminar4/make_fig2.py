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

fig, ax = plt.subplots(figsize=(16.2, 9.4))
ax.set_xlim(0, 16.2)
ax.set_ylim(0, 9.4)
ax.axis("off")

colors = {
    "demand": ("#DDEAF3", "#2B6F9E"),
    "fulfil": ("#E4F0E4", "#3B7D3A"),
    "resource": ("#F7E9DC", "#C96C22"),
    "analytics": ("#ECE6F3", "#6B4C8A"),
    "line": "#333333",
    "panel": "#F7F8FA",
    "panel_edge": "#C8CDD3",
}

W, H = 1.92, 0.78

panels = {
    "demand": (0.55, 5.15, 7.55, 3.55, "A. Demand and membership relationships"),
    "fulfil": (8.55, 5.15, 7.55, 3.55, "B. Order fulfilment relationships"),
    "supply": (0.55, 1.15, 7.55, 3.55, "C. Product and supply relationships"),
    "analytics": (8.55, 1.15, 7.55, 3.55, "D. Analytical feedback relationships"),
}

for x, y, w, h, title in panels.values():
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.10,rounding_size=0.14",
        linewidth=0.9,
        edgecolor=colors["panel_edge"],
        facecolor=colors["panel"],
        zorder=0,
    ))
    ax.text(x + 0.16, y + h - 0.20, title, fontsize=11.0, fontweight="bold", va="top", color="#222222", zorder=5)

nodes = {}

def add_node(key, x, y, category, title, example):
    fill, edge = colors[category]
    nodes[key] = (x, y)
    ax.add_patch(FancyBboxPatch(
        (x - W / 2, y - H / 2), W, H,
        boxstyle="round,pad=0.08,rounding_size=0.10",
        linewidth=1.05,
        edgecolor=edge,
        facecolor=fill,
        zorder=3,
    ))
    ax.text(x, y + 0.19, title, ha="center", va="center", fontsize=9.4, fontweight="bold", color="#111111", zorder=4)
    ax.text(x, y - 0.02, f"({example})", ha="center", va="center", fontsize=6.9, color="#222222", zorder=4)
    ax.text(x, y - 0.25, "CV / SV / AV / EP", ha="center", va="center", fontsize=6.2, color="#444444", zorder=4)

def anchor(key, side):
    x, y = nodes[key]
    if side == "r":
        return x + W / 2, y
    if side == "l":
        return x - W / 2, y
    if side == "t":
        return x, y + H / 2
    if side == "b":
        return x, y - H / 2
    return x, y

def draw_label(x, y, rel, card):
    ax.text(
        x, y, f"{rel}  {card}",
        ha="center",
        va="center",
        fontsize=7.4,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="#CCCCCC", linewidth=0.25, alpha=0.96),
        zorder=8,
    )

def arrow(a, aside, b, bside, rel, card, dashed=False, rad=0, label_shift=(0, 0)):
    p1, p2 = anchor(a, aside), anchor(b, bside)
    ax.add_patch(FancyArrowPatch(
        p1, p2,
        arrowstyle="-|>",
        mutation_scale=10.5,
        linewidth=1.0,
        color=colors["line"],
        linestyle=(0, (4, 3)) if dashed else "solid",
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=3,
        shrinkB=3,
        zorder=2,
    ))
    draw_label((p1[0] + p2[0]) / 2 + label_shift[0], (p1[1] + p2[1]) / 2 + label_shift[1], rel, card)

def poly_arrow(points, rel, card, dashed=False, label_index=0, label_shift=(0, 0)):
    style = (0, (4, 3)) if dashed else "solid"
    for i in range(len(points) - 1):
        ax.add_patch(FancyArrowPatch(
            points[i], points[i + 1],
            arrowstyle="-|>" if i == len(points) - 2 else "-",
            mutation_scale=10.5,
            linewidth=1.0,
            color=colors["line"],
            linestyle=style,
            shrinkA=0,
            shrinkB=3 if i == len(points) - 2 else 0,
            zorder=2,
        ))
    p1, p2 = points[label_index], points[label_index + 1]
    draw_label((p1[0] + p2[0]) / 2 + label_shift[0], (p1[1] + p2[1]) / 2 + label_shift[1], rel, card)

# Panel A
add_node("A_channel", 1.55, 7.25, "demand", "Digital Channel", "app, mini-program")
add_node("A_customer", 3.75, 7.25, "demand", "Customer", "member, commuter")
add_node("A_member", 5.95, 7.25, "demand", "Membership Account", "points, coupons")
add_node("A_promo", 3.75, 6.05, "resource", "Promotion Campaign", "coupon, offer")
add_node("A_order", 5.95, 6.05, "analytics", "Digital Order", "pickup, delivery")
arrow("A_channel", "r", "A_customer", "l", "D1", "1:N")
arrow("A_customer", "r", "A_member", "l", "D2", "1:1")
arrow("A_member", "b", "A_order", "t", "D3", "1:N", label_shift=(0.38, 0.05))
arrow("A_promo", "t", "A_member", "b", "D4", "M:N", label_shift=(-0.48, 0.18))
arrow("A_promo", "r", "A_order", "l", "D5", "M:N", label_shift=(0, -0.18))

# Panel B
add_node("B_order", 9.85, 7.25, "analytics", "Digital Order", "pickup, delivery")
add_node("B_task", 12.15, 7.25, "fulfil", "Fulfilment Task", "prepare, handover")
add_node("B_store", 14.45, 7.25, "fulfil", "Store", "self-operated, partner")
add_node("B_item", 9.85, 6.05, "analytics", "Order Item", "drink line, add-on")
add_node("B_staff", 14.45, 6.05, "fulfil", "Store Staff", "barista, manager")
add_node("B_delivery", 12.15, 6.05, "resource", "Delivery Partner", "courier, platform")
arrow("B_order", "r", "B_task", "l", "F2", "1:N")
arrow("B_task", "r", "B_store", "l", "F3", "N:1")
arrow("B_order", "b", "B_item", "t", "F1", "1:N")
arrow("B_store", "b", "B_staff", "t", "F4", "1:N")
poly_arrow([anchor("B_store", "b"), (14.45, 5.55), (12.15, 5.55), anchor("B_delivery", "b")], "F5", "1:N", label_index=1)

# Panel C
add_node("C_item", 1.55, 3.40, "analytics", "Order Item", "drink line, add-on")
add_node("C_product", 3.75, 3.40, "demand", "Product", "coffee, light food")
add_node("C_recipe", 5.95, 3.40, "demand", "Recipe Standard", "dosage, SOP")
add_node("C_material", 5.95, 2.20, "resource", "Raw Material", "beans, milk")
add_node("C_supplier", 3.75, 2.20, "resource", "Supplier", "farm, vendor")
add_node("C_store", 1.55, 2.20, "fulfil", "Store", "inventory location")
arrow("C_item", "r", "C_product", "l", "S1", "N:1")
arrow("C_product", "r", "C_recipe", "l", "S2", "1:N")
arrow("C_recipe", "b", "C_material", "t", "S3", "M:N")
arrow("C_supplier", "r", "C_material", "l", "S4", "1:N")
arrow("C_material", "l", "C_store", "r", "S5", "M:N")

# Panel D
add_node("D_order", 9.85, 3.40, "analytics", "Digital Order", "revenue, order value")
add_node("D_store", 12.15, 3.40, "fulfil", "Store", "margin, stockout")
add_node("D_delivery", 14.45, 3.40, "resource", "Delivery Partner", "time, cost")
add_node("D_perf", 12.15, 2.20, "analytics", "Performance Result", "KPI dashboard")
add_node("D_promo", 14.45, 2.20, "resource", "Promotion Campaign", "future targeting")
arrow("D_order", "b", "D_perf", "l", "A1", "1:N", dashed=True, rad=-0.12, label_shift=(-0.36, -0.12))
arrow("D_store", "b", "D_perf", "t", "A2", "1:N", dashed=True, label_shift=(0, 0.10))
arrow("D_delivery", "b", "D_perf", "r", "A3", "1:N", dashed=True, rad=0.12, label_shift=(0.36, -0.12))
arrow("D_perf", "r", "D_promo", "l", "A4", "1:N", dashed=True)

# Legend
legend_y = 0.78
ax.text(0.65, legend_y, "Legend:", ha="left", va="center", fontsize=9.6, fontweight="bold")
legend_items = [
    ("demand", "Demand/customer"),
    ("analytics", "Transaction/analytics"),
    ("fulfil", "Fulfilment"),
    ("resource", "Resource/partner"),
]
for i, (cat, label) in enumerate(legend_items):
    fill, edge = colors[cat]
    x = 1.55 + i * 2.25
    ax.add_patch(Rectangle((x, legend_y - 0.10), 0.22, 0.16, facecolor=fill, edgecolor=edge, linewidth=0.8))
    ax.text(x + 0.30, legend_y - 0.02, label, ha="left", va="center", fontsize=8.2)

ax.text(10.75, legend_y, "IDs: D demand | F fulfilment | S supply | A analytics", ha="left", va="center", fontsize=8.2)
ax.text(10.75, legend_y - 0.32, "Multiplicity: 1:1, 1:N, N:1, M:N", ha="left", va="center", fontsize=8.2)
ax.plot([13.55, 14.00], [legend_y - 0.32, legend_y - 0.32], color=colors["line"], lw=1.0)
ax.text(14.08, legend_y - 0.32, "operational", ha="left", va="center", fontsize=8.2)
ax.plot([15.00, 15.45], [legend_y - 0.32, legend_y - 0.32], color=colors["line"], lw=1.0, linestyle=(0, (4, 3)))
ax.text(15.53, legend_y - 0.32, "feedback", ha="left", va="center", fontsize=8.2)

ax.text(8.10, 0.34, "Each repeated boundary object represents the same business object in a different relationship group; CV/SV/AV/EP follow the seminar notation.", ha="center", va="center", fontsize=8.7, color="#333333")

fig.tight_layout(pad=0.2)
fig.savefig(OUT, format="pdf", bbox_inches="tight")
print(OUT)
