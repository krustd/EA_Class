from pathlib import Path

code = r'''
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.lines import Line2D

OUT_DIR = Path("/mnt/data")
PNG = OUT_DIR / "luckin_conceptual_model_recreated.png"
PDF = OUT_DIR / "luckin_conceptual_model_recreated.pdf"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.unicode_minus": False,
})

BLUE = "#2563eb"
RED = "#dc2626"
BLACK = "#111827"
GRAY = "#6b7280"
BOX = "#ffffff"
EDGE = "#111827"

fig, ax = plt.subplots(figsize=(18, 13), dpi=180)
ax.set_xlim(0, 18)
ax.set_ylim(0, 13)
ax.axis("off")


def draw_rich_text_line(ax, x, y, parts, size=9):
    """Draw a line made of colored segments in data coordinates."""
    fig = ax.figure
    renderer = fig.canvas.get_renderer()
    cur_x = x
    for text, color, weight in parts:
        t = ax.text(cur_x, y, text, fontsize=size, color=color, fontweight=weight,
                    ha="left", va="center")
        fig.canvas.draw_idle()
        bbox = t.get_window_extent(renderer=renderer)
        # convert pixel width to data-width
        p0 = ax.transData.transform((cur_x, y))
        p1 = (p0[0] + bbox.width, p0[1])
        cur_x = ax.transData.inverted().transform(p1)[0]


def box(ax, key, x, y, w, h, title, kind, attrs):
    rect = Rectangle((x, y), w, h, facecolor=BOX, edgecolor=EDGE, linewidth=1.2)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 0.18, title, ha="center", va="top",
            fontsize=10, fontweight="bold", color=BLACK)
    ax.text(x + w/2, y + h - 0.45, f"({kind})", ha="center", va="top",
            fontsize=9, color=BLACK)

    yy = y + h - 0.95
    for role, name in attrs:
        if role == "x":
            parts = [("x  ", BLACK, "normal"), (name, BLUE, "normal")]
        elif role == ".sum":
            parts = [(".sum  ", RED, "normal"), (name, BLACK, "normal")]
        elif role == ".count":
            parts = [(".count  ", RED, "normal"), (name, BLACK, "normal")]
        elif role == ".estimated":
            parts = [(".estimated  ", BLUE, "normal"), (name, BLACK, "normal")]
        else:
            parts = [(name, BLACK, "normal")]
        draw_rich_text_line(ax, x + 0.18, yy, parts, size=8.7)
        yy -= 0.28

    boxes[key] = (x, y, w, h)


def anchor(key, side):
    x, y, w, h = boxes[key]
    if side == "left":
        return (x, y + h/2)
    if side == "right":
        return (x + w, y + h/2)
    if side == "top":
        return (x + w/2, y + h)
    if side == "bottom":
        return (x + w/2, y)
    raise ValueError(side)


def arrow_between(a, aside, b, bside, label="", dashed=True, rad=0.0, lw=1.2):
    start = anchor(a, aside)
    end = anchor(b, bside)
    style = "->"
    patch = FancyArrowPatch(
        start, end,
        arrowstyle=style,
        mutation_scale=11,
        linewidth=lw,
        color=BLACK,
        linestyle=(0, (3, 3)) if dashed else "solid",
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=4,
        shrinkB=4,
    )
    ax.add_patch(patch)
    if label:
        mx = (start[0] + end[0]) / 2
        my = (start[1] + end[1]) / 2
        ax.text(mx, my + 0.16, label, fontsize=8.8, ha="center", va="bottom",
                bbox=dict(facecolor="white", edgecolor="none", pad=0.5))


def elbow_arrow(points, label="", dashed=True):
    # draw segmented polyline, arrow on final segment
    for i in range(len(points) - 2):
        ax.add_line(Line2D([points[i][0], points[i+1][0]],
                           [points[i][1], points[i+1][1]],
                           color=BLACK, linewidth=1.15,
                           linestyle=(0, (3, 3)) if dashed else "solid"))
    patch = FancyArrowPatch(points[-2], points[-1], arrowstyle="->", mutation_scale=11,
                            linewidth=1.15, color=BLACK,
                            linestyle=(0, (3, 3)) if dashed else "solid",
                            shrinkA=0, shrinkB=4)
    ax.add_patch(patch)
    if label:
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        ax.text(sum(xs)/len(xs), sum(ys)/len(ys)+0.14, label, fontsize=8.8,
                ha="center", va="bottom", bbox=dict(facecolor="white", edgecolor="none", pad=0.5))


# Title
ax.text(0.45, 12.65, "LUCKIN COFFEE – Conceptual Model", fontsize=16,
        fontweight="bold", ha="left", va="top", color=BLACK)

# Legend
legend_x, legend_y = 0.45, 12.12
ax.text(legend_x, legend_y, "LEGEND:", fontsize=10.5, fontweight="bold", ha="left", va="top")
legend_lines = [
    ("one-to-many relationship", "<-"),
    ("many-to-one relationship", "->"),
    ("one-to-one relationship", "<->"),
    ("many-to-many relationship", "<->"),
    ("reading direction", "-->"),
]
yy = legend_y - 0.45
for txt, _ in legend_lines:
    ax.add_line(Line2D([legend_x, legend_x+1.55], [yy, yy], color=BLACK, linewidth=1.0,
                       linestyle=(0, (3, 3)) if txt == "reading direction" else "solid"))
    ax.text(legend_x + 1.85, yy, txt, fontsize=9.2, va="center", ha="left")
    yy -= 0.28

draw_rich_text_line(ax, legend_x, 10.45, [("x ", BLUE, "normal"), ("variable", BLUE, "normal"),
                     (": indicates that the variable has a classifying role", BLACK, "normal")], size=8.7)
draw_rich_text_line(ax, legend_x, 10.20, [(".count ", RED, "normal"),
                     (": indicates that the Object objects are counted", BLACK, "normal")], size=8.7)
draw_rich_text_line(ax, legend_x, 9.95, [(".sum ", RED, "normal"),
                     (": indicates that the Variable is summarised", BLACK, "normal")], size=8.7)
draw_rich_text_line(ax, legend_x, 9.70, [(".estimated ", BLUE, "normal"),
                     (": indicates that the Variable is estimated", BLACK, "normal")], size=8.7)

boxes = {}

# Nodes
box(ax, "customer", 0.45, 7.85, 3.0, 1.75, "Customer", "Actor",
    [("x", "Segment"), ("x", "City"), ("x", "AgeBand"),
     (".estimated", "CLV"), (".estimated", "RepeatPurchRate")])

box(ax, "member", 5.1, 7.85, 2.85, 1.75, "MembershipAccount", "Utility",
    [("x", "MemberTier"), ("x", "ActivityStatus"),
     (".sum", "PointsBalance"), (".sum", "CouponValue"), (".count", "Account")])

box(ax, "campaign", 9.0, 7.85, 3.05, 1.75, "PromotionCampaign", "Event",
    [("x", "CampaignType"), ("x", "TargetSegment"), ("x", "ValidPeriod"),
     (".sum", "SubsidyAmount"), (".estimated", "RedemptionRate")])

box(ax, "channel", 13.35, 7.85, 3.0, 1.75, "DigitalChannel", "Interface",
    [("x", "ChannelType"), ("x", "AccessDevice"), ("x", "AppVersion"),
     (".sum", "PaymentAmount"), (".estimated", "ConversionRate")])

box(ax, "system", 12.9, 10.55, 3.95, 2.35, "LuckinCoffeeSystem", "Utility",
    [("", "- Country"), ("", "- Currency"), ("", "- CompulsoryEdBegAge"),
     ("", "- CompulsoryEdEndAge"), ("", "- CompulsoryEdLength"),
     ("", "- AcadYearBegMonth"), ("", "- AcadYearEndMonth")])

box(ax, "order", 13.35, 4.65, 3.0, 2.15, "DigitalOrder", "Transaction",
    [("x", "OrderChannel"), ("x", "PaymentMethod"), ("x", "QueueStatus"),
     (".sum", "OrderAmount"), (".sum", "DeliveryFee"),
     (".estimated", "AOV"), (".count", "Order")])

box(ax, "task", 6.15, 4.85, 3.05, 1.7, "FulfilmentTask", "Event",
    [("x", "TaskType"), (".sum", "PrepTime"),
     (".sum", "WaitingTime"), (".estimated", "CompletionRate")])

box(ax, "store", 6.25, 2.4, 3.15, 1.75, "Store", "Establishment",
    [("x", "OwnershipType"), ("x", "CityTier"), ("x", "LocationType"),
     (".sum", "Revenue"), (".estimated", "UtilisationRate")])

box(ax, "partner", 10.05, 3.55, 2.75, 1.5, "DeliveryPartner", "Provider",
    [("x", "ServiceArea"), ("x", "PartnerType"),
     (".sum", "DeliveryFee"), (".estimated", "ComplaintRate")])

box(ax, "staff", 13.85, 1.85, 2.65, 1.65, "StoreStaff", "Actor",
    [("x", "StaffRole"), ("x", "TrainingStatus"),
     (".sum", "LabourCost"), (".sum", "WorkingHours"),
     (".estimated", "Productivity")])

box(ax, "raw", 5.7, 0.85, 3.15, 1.75, "RawMaterial", "Resource",
    [("x", "MaterialType"), ("x", "Origin"), ("x", "BatchStatus"),
     (".sum", "InventoryValue"), (".estimated", "StockoutRate")])

box(ax, "supplier", 10.2, 0.85, 2.85, 1.5, "Supplier", "Provider",
    [("x", "SupplierType"), ("x", "LeadTime"),
     (".sum", "PurchaseCost"), (".estimated", "QualityPassRate")])

box(ax, "recipe", 0.45, 1.05, 3.0, 1.65, "RecipeStandard", "Utility",
    [("x", "RecipeVersion"), ("x", "SOPStatus"),
     (".sum", "StandardCost"), (".estimated", "DefectRate")])

box(ax, "product", 0.45, 3.7, 2.75, 1.45, "Product", "Commodity",
    [("x", "Category"), ("x", "Season"),
     (".estimated", "GrossMargin")])

box(ax, "item", 0.45, 5.45, 2.75, 1.35, "OrderItem", "Transaction",
    [("x", "ProductCategory"), (".sum", "ItemPrice"),
     (".estimated", "ItemShare")])

# Relationships
arrow_between("customer", "right", "member", "left", "Owned by")
arrow_between("member", "right", "campaign", "left", "Targets")
arrow_between("campaign", "right", "channel", "left", "Applied to")
arrow_between("channel", "top", "system", "bottom", "BelongsTo", dashed=False)
arrow_between("channel", "bottom", "order", "top", "Via")

arrow_between("member", "bottom", "task", "top", "Placed by")
arrow_between("order", "left", "task", "right", "Fulfils", dashed=False)
arrow_between("partner", "right", "order", "left", "Assigned to")
arrow_between("store", "top", "task", "bottom", "Executed at")

arrow_between("item", "right", "task", "left", "Belongs to", dashed=False)
arrow_between("item", "bottom", "product", "top", "Refers to")
arrow_between("recipe", "top", "product", "bottom", "Defined by", dashed=False)
arrow_between("recipe", "right", "raw", "left", "Consumes", dashed=False)
arrow_between("raw", "top", "store", "bottom", "Stocked at")
arrow_between("supplier", "left", "raw", "right", "Provided by")
# Optional relation implied by layout: staff operates store
elbow_arrow([(15.15, 3.5), (15.15, 4.1), (9.4, 4.1)], label="", dashed=True)

# Light visual grouping / reading guide
ax.text(0.55, 0.35, "Reading direction: Customer & Membership → Campaign & Channel → Order → Fulfilment → Store / Material / Supplier",
        fontsize=9.5, color=GRAY, ha="left", va="center")

plt.tight_layout()
fig.savefig(PNG, bbox_inches="tight", pad_inches=0.15)
fig.savefig(PDF, bbox_inches="tight", pad_inches=0.15)
plt.close(fig)

# Also export this exact script
SCRIPT = OUT_DIR / "draw_luckin_conceptual_model.py"
SCRIPT.write_text(code if "code" in globals() else "", encoding="utf-8")
print(f"Saved:\n- {PNG}\n- {PDF}\n- {SCRIPT}")
'''

# Write script and execute it
script_path = Path("/mnt/data/draw_luckin_conceptual_model.py")
script_path.write_text(code, encoding="utf-8")
exec(compile(code, str(script_path), "exec"))
print(f"Script saved: {script_path}")