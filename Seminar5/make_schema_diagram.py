from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.path import Path as MplPath

BASE_DIR = Path(__file__).resolve().parent
FIG_DIR = BASE_DIR / "fig"
FIG_DIR.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

HEADER = "#C00000"
BORDER = "#333333"
LINE = "#303030"
BG = "#F7F8FA"
W = 3.55
ROW_H = 0.38
HEAD_H = 0.52


def draw_diagram(path, title, table_specs, connectors, size=(18, 10), xlim=(0, 18), ylim=(0, 10)):
    fig, ax = plt.subplots(figsize=size)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    ax.set_facecolor("white")
    nodes = {}

    ax.add_patch(FancyBboxPatch(
        (xlim[0] + 0.25, ylim[0] + 0.35),
        xlim[1] - xlim[0] - 0.5,
        ylim[1] - ylim[0] - 0.9,
        boxstyle="round,pad=0.04,rounding_size=0.08",
        facecolor=BG,
        edgecolor="#CBD3DC",
        linewidth=1.0,
        zorder=0,
    ))
    ax.text((xlim[0] + xlim[1]) / 2, ylim[1] - 0.35, title,
            ha="center", va="center", fontsize=20, fontweight="bold")

    def table(x, y, name, cols, pk_rows):
        h = HEAD_H + len(cols) * ROW_H
        ax.add_patch(FancyBboxPatch(
            (x, y - h), W, h,
            boxstyle="round,pad=0.00,rounding_size=0.025",
            facecolor="white",
            edgecolor=BORDER,
            linewidth=0.9,
            zorder=3,
        ))
        ax.add_patch(FancyBboxPatch(
            (x, y - HEAD_H), W, HEAD_H,
            boxstyle="round,pad=0.00,rounding_size=0.025",
            facecolor=HEADER,
            edgecolor=BORDER,
            linewidth=0.9,
            zorder=4,
        ))
        ax.text(x + W / 2, y - HEAD_H / 2, name, color="white", ha="center", va="center",
                fontsize=11.3, fontweight="bold", zorder=5)

        for i, col in enumerate(cols):
            row_y = y - HEAD_H - (i + 1) * ROW_H
            ax.plot([x, x + W], [row_y, row_y], color="#D9D9D9", lw=0.6, zorder=4)
            is_pk = i in pk_rows
            ax.text(x + 0.16, row_y + ROW_H / 2, col, ha="left", va="center",
                    fontsize=8.8, fontweight="bold" if is_pk else "normal", zorder=5)
            if is_pk:
                ax.plot([x + 0.16, x + min(W - 0.2, 0.16 + len(col) * 0.077)],
                        [row_y + 0.083, row_y + 0.083], color="black", lw=0.8, zorder=5)

        nodes[name] = {
            "left": (x, y - h / 2),
            "right": (x + W, y - h / 2),
            "top": (x + W / 2, y),
            "bottom": (x + W / 2, y - h),
        }

    def card_position(point, side, away_from_table=True):
        offsets = {
            "left": (-0.22, 0.12),
            "right": (0.22, 0.12),
            "top": (0.0, 0.22),
            "bottom": (0.0, -0.22),
        }
        dx, dy = offsets.get(side, (0.0, 0.0))
        if not away_from_table:
            dx, dy = -dx, -dy
        return point[0] + dx, point[1] + dy

    def cardinality_label(point, side, text, away_from_table=True):
        x, y = card_position(point, side, away_from_table)
        ax.text(x, y, text, fontsize=10.5, fontweight="bold", color="black",
                ha="center", va="center", zorder=7,
                bbox=dict(facecolor="white", edgecolor="#555555", linewidth=0.45,
                          boxstyle="round,pad=0.12", alpha=0.98))

    def connect(src, dst, start="right", end="left", via=None, start_card=None, end_card=None):
        points = [nodes[src][start]]
        if via:
            points.extend(via)
        points.append(nodes[dst][end])
        codes = [MplPath.MOVETO] + [MplPath.LINETO] * (len(points) - 1)
        ax.add_patch(FancyArrowPatch(
            path=MplPath(points, codes),
            arrowstyle="-|>",
            mutation_scale=11,
            linewidth=1.05,
            color=LINE,
            shrinkA=4,
            shrinkB=4,
            zorder=2,
        ))
        if start_card:
            cardinality_label(points[0], start, start_card)
        if end_card:
            cardinality_label(points[-1], end, end_card)

    for spec in table_specs:
        table(*spec)
    for spec in connectors:
        connect(*spec)

    ax.text((xlim[0] + xlim[1]) / 2, ylim[0] + 0.12,
            "Underlined attributes are primary keys. Arrows point from foreign keys to referenced keys; endpoint labels show relationship cardinality. Bridge tables resolve M:N relationships.",
            ha="center", va="center", fontsize=10.5, style="italic")

    fig.savefig(path, format="pdf", bbox_inches="tight")
    plt.close(fig)


operations_tables = [
    (0.75, 8.75, "Customers", ["CustomerId", "Segment", "City", "AgeBand"], [0]),
    (0.75, 5.85, "DigitalChannels", ["ChannelId", "ChannelType", "AccessDevice", "AppVersion"], [0]),
    (0.75, 3.0, "PromotionCampaigns", ["CampaignId", "CampaignType", "TargetSegment", "StartDate", "EndDate"], [0]),

    (4.55, 8.75, "MembershipAccounts", ["MemberId", "CustomerId FK", "PointsBalance", "MemberTier", "ActivityStatus"], [0]),
    (4.55, 3.0, "MemberCampaigns", ["MemberId FK", "CampaignId FK", "ReceivedDate", "UsedStatus"], [0, 1]),

    (8.35, 8.75, "DigitalOrders", ["OrderId", "MemberId FK", "ChannelId FK", "PaymentMethod", "QueueStatus", "GrossOrderAmount", "NetPayableAmount", "OrderDate/Time"], [0]),
    (8.35, 3.0, "OrderCampaigns", ["OrderId FK", "MemberId FK", "CampaignId FK", "AppliedAmount"], [0, 2]),

    (12.15, 8.75, "OrderItems", ["OrderId FK", "ItemNr", "ProductId FK", "Quantity", "Customization", "UnitItemPrice"], [0, 1]),
    (12.15, 4.95, "FulfilmentTasks", ["TaskId", "OrderId FK", "StoreId FK", "PartnerId FK", "TaskType", "Status"], [0]),

    (15.95, 8.75, "Products", ["ProductId", "ProductName", "Category", "GrossMargin"], [0]),
    (15.95, 5.55, "Stores", ["StoreId", "StoreName", "OwnershipType", "CityTier", "Revenue"], [0]),
    (15.95, 2.45, "DeliveryPartners", ["PartnerId", "PartnerName", "PartnerType", "ServiceArea", "ComplaintRate"], [0]),
]

operations_connectors = [
    ("MembershipAccounts", "Customers", "left", "right", None, "1", "1"),
    ("DigitalOrders", "MembershipAccounts", "left", "right", None, "N", "1"),
    ("DigitalOrders", "DigitalChannels", "left", "right", [(7.2, 5.05)], "N", "1"),
    ("MemberCampaigns", "MembershipAccounts", "top", "bottom", None, "N", "1"),
    ("MemberCampaigns", "PromotionCampaigns", "left", "right", None, "N", "1"),
    ("OrderCampaigns", "DigitalOrders", "top", "bottom", None, "N", "1"),
    ("OrderCampaigns", "MemberCampaigns", "left", "right", None, "N", "1"),
    ("OrderItems", "DigitalOrders", "left", "right", None, "N", "1"),
    ("FulfilmentTasks", "DigitalOrders", "left", "right", [(11.75, 6.2)], "N", "1"),
    ("OrderItems", "Products", "right", "left", None, "N", "1"),
    ("FulfilmentTasks", "Stores", "right", "left", None, "N", "1"),
    ("FulfilmentTasks", "DeliveryPartners", "right", "left", [(14.65, 3.2)], "N", "1"),
]

supply_tables = [
    (0.9, 8.45, "Products", ["ProductId", "ProductName", "Category", "Season", "GrossMargin", "CurrentStandardCost"], [0]),
    (0.9, 4.25, "Stores", ["StoreId", "StoreName", "OwnershipType", "CityTier", "Revenue", "LaborCost"], [0]),

    (5.25, 8.45, "RecipeStandards", ["RecipeId", "ProductId FK", "RecipeVersion", "SopStatus", "RecipeStandardCost", "EffectiveFrom/To"], [0]),
    (5.25, 4.25, "StoreMaterials", ["StoreId FK", "MaterialId FK", "StockLevel", "StockoutRate"], [0, 1]),

    (9.6, 8.45, "RecipeMaterials", ["RecipeId FK", "MaterialId FK", "DosageAmount", "DosageUnit"], [0, 1]),
    (9.6, 4.25, "RawMaterials", ["MaterialId", "SupplierId FK", "MaterialName", "MaterialType", "Origin", "BatchStatus", "InventoryValue"], [0]),

    (13.95, 6.35, "Suppliers", ["SupplierId", "SupplierName", "SupplierType", "LeadTime"], [0]),
]

supply_connectors = [
    ("RecipeStandards", "Products", "left", "right", None, "N", "1"),
    ("RecipeMaterials", "RecipeStandards", "left", "right", None, "N", "1"),
    ("RecipeMaterials", "RawMaterials", "bottom", "top", None, "N", "1"),
    ("StoreMaterials", "Stores", "left", "right", None, "N", "1"),
    ("StoreMaterials", "RawMaterials", "right", "left", None, "N", "1"),
    ("RawMaterials", "Suppliers", "right", "left", None, "N", "1"),
]


def main():
    draw_diagram(
        FIG_DIR / "schema_operations.pdf",
        "Luckin Coffee Relational Data Model: Customer, Order and Fulfilment",
        operations_tables,
        operations_connectors,
        size=(21, 10.5),
        xlim=(0, 19.8),
        ylim=(0, 10),
    )
    draw_diagram(
        FIG_DIR / "schema_supply.pdf",
        "Luckin Coffee Relational Data Model: Product, Recipe and Supply",
        supply_tables,
        supply_connectors,
        size=(18, 10),
        xlim=(0, 17.8),
        ylim=(0, 10),
    )
    print(f"Generated schema diagrams at: {FIG_DIR / 'schema_operations.pdf'} and {FIG_DIR / 'schema_supply.pdf'}")


if __name__ == "__main__":
    main()
