import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch

os.makedirs("/Users/cccsh/Desktop/EA_Class/Seminar5/fig", exist_ok=True)
OUT = "/Users/cccsh/Desktop/EA_Class/Seminar5/fig/schema.pdf"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

fig, ax = plt.subplots(figsize=(24, 16))
ax.set_xlim(0, 24)
ax.set_ylim(0, 16)
ax.axis("off")

RED_HEADER = "#C00000"
TEXT_COLOR = "white"
LINE_COLOR = "#333333"

TABLE_W = 3.5
ROW_H = 0.35
HEADER_H = 0.45

col_coords = {}

def draw_vertical_table(x, y, table_name, columns, pk_indices):
    """
    x, y is the top-left corner of the table.
    Draws a vertical table with table_name in the header, and columns as rows.
    """
    n_cols = len(columns)
    table_h = HEADER_H + n_cols * ROW_H
    
    # Header
    rect = Rectangle((x, y - HEADER_H), TABLE_W, HEADER_H, facecolor=RED_HEADER, edgecolor="black", linewidth=0.8)
    ax.add_patch(rect)
    ax.text(x + TABLE_W/2, y - HEADER_H/2, table_name, color=TEXT_COLOR, 
            ha="center", va="center", fontsize=11, fontweight="bold")
            
    # Rows
    for i, col in enumerate(columns):
        ry = y - HEADER_H - (i + 1) * ROW_H
        rect = Rectangle((x, ry), TABLE_W, ROW_H, facecolor="white", edgecolor="black", linewidth=0.5)
        ax.add_patch(rect)
        
        is_pk = i in pk_indices
        font_weight = "bold" if is_pk else "normal"
        ax.text(x + 0.15, ry + ROW_H/2, col, color="black", 
                ha="left", va="center", fontsize=9, fontweight=font_weight)
        
        if is_pk:
            ax.plot([x + 0.15, x + 0.15 + len(col)*0.08], [ry + 0.08, ry + 0.08], color="black", lw=0.8)
            
        col_coords[(table_name, col)] = {
            "left": (x, ry + ROW_H/2),
            "right": (x + TABLE_W, ry + ROW_H/2),
            "top": (x + TABLE_W/2, ry + ROW_H),
            "bottom": (x + TABLE_W/2, ry)
        }
        
    return table_h

tables_info = {
    "Customers": {"cols": ["CustomerId", "Segment", "City", "AgeBand"], "pk": [0]},
    "MembershipAccounts": {"cols": ["MemberId", "CustomerId", "PointsBalance", "CouponValue", "MemberTier", "ActivityStatus"], "pk": [0]},
    "DigitalChannels": {"cols": ["ChannelId", "ChannelType", "AccessDevice", "AppVersion"], "pk": [0]},
    "PromotionCampaigns": {"cols": ["CampaignId", "CampaignType", "TargetSegment", "ValidPeriod", "SubsidyAmount"], "pk": [0]},
    "MemberCampaigns": {"cols": ["MemberId", "CampaignId", "ReceivedDate", "UsedStatus"], "pk": [0, 1]},
    "DigitalOrders": {"cols": ["OrderId", "MemberId", "ChannelId", "OrderChannel", "PaymentMethod", "QueueStatus", "OrderAmount", "DeliveryFee", "OrderDate", "OrderTime"], "pk": [0]},
    "OrderCampaigns": {"cols": ["OrderId", "CampaignId", "AppliedAmount"], "pk": [0, 1]},
    "OrderItems": {"cols": ["OrderId", "ItemNr", "ProductId", "Quantity", "Customization", "Discount", "ItemPrice"], "pk": [0, 1]},
    "Products": {"cols": ["ProductId", "ProductName", "Category", "Season", "GrossMargin", "StandardCost"], "pk": [0]},
    "RecipeStandards": {"cols": ["RecipeId", "ProductId", "RecipeVersion", "SopStatus", "StandardCost", "DefectRate"], "pk": [0]},
    "RecipeMaterials": {"cols": ["RecipeId", "MaterialId", "Dosage"], "pk": [0, 1]},
    "RawMaterials": {"cols": ["MaterialId", "SupplierId", "MaterialName", "MaterialType", "Origin", "BatchStatus", "InventoryValue"], "pk": [0]},
    "Suppliers": {"cols": ["SupplierId", "SupplierName", "SupplierType", "LeadTime"], "pk": [0]},
    "Stores": {"cols": ["StoreId", "StoreName", "OwnershipType", "CityTier", "LocationType", "Revenue", "LaborCost"], "pk": [0]},
    "StoreStaff": {"cols": ["StaffId", "StoreId", "StaffName", "StaffRole", "TrainingStatus", "WorkingHours", "LaborCost", "Productivity"], "pk": [0]},
    "StoreMaterials": {"cols": ["StoreId", "MaterialId", "StockLevel", "StockoutRate"], "pk": [0, 1]},
    "FulfilmentTasks": {"cols": ["TaskId", "OrderId", "StoreId", "PartnerId", "TaskType", "PrepTime", "WaitingTime", "CompletionRate", "Status"], "pk": [0]},
    "DeliveryPartners": {"cols": ["PartnerId", "PartnerName", "PartnerType", "ServiceArea", "DeliveryFee", "ComplaintRate"], "pk": [0]}
}

# Col 1
draw_vertical_table(0.5, 15.0, "Customers", tables_info["Customers"]["cols"], tables_info["Customers"]["pk"])
draw_vertical_table(0.5, 12.0, "MembershipAccounts", tables_info["MembershipAccounts"]["cols"], tables_info["MembershipAccounts"]["pk"])
draw_vertical_table(0.5, 8.0, "DigitalChannels", tables_info["DigitalChannels"]["cols"], tables_info["DigitalChannels"]["pk"])

# Col 2
draw_vertical_table(5.5, 15.0, "MemberCampaigns", tables_info["MemberCampaigns"]["cols"], tables_info["MemberCampaigns"]["pk"])
draw_vertical_table(5.5, 12.0, "DigitalOrders", tables_info["DigitalOrders"]["cols"], tables_info["DigitalOrders"]["pk"])
draw_vertical_table(5.5, 6.5, "OrderCampaigns", tables_info["OrderCampaigns"]["cols"], tables_info["OrderCampaigns"]["pk"])
draw_vertical_table(5.5, 3.5, "PromotionCampaigns", tables_info["PromotionCampaigns"]["cols"], tables_info["PromotionCampaigns"]["pk"])

# Col 3
draw_vertical_table(10.5, 15.0, "FulfilmentTasks", tables_info["FulfilmentTasks"]["cols"], tables_info["FulfilmentTasks"]["pk"])
draw_vertical_table(10.5, 10.0, "OrderItems", tables_info["OrderItems"]["cols"], tables_info["OrderItems"]["pk"])
draw_vertical_table(10.5, 5.0, "DeliveryPartners", tables_info["DeliveryPartners"]["cols"], tables_info["DeliveryPartners"]["pk"])

# Col 4
draw_vertical_table(15.5, 15.0, "Stores", tables_info["Stores"]["cols"], tables_info["Stores"]["pk"])
draw_vertical_table(15.5, 10.0, "Products", tables_info["Products"]["cols"], tables_info["Products"]["pk"])
draw_vertical_table(15.5, 5.5, "RecipeMaterials", tables_info["RecipeMaterials"]["cols"], tables_info["RecipeMaterials"]["pk"])
draw_vertical_table(15.5, 2.0, "Suppliers", tables_info["Suppliers"]["cols"], tables_info["Suppliers"]["pk"])

# Col 5
draw_vertical_table(20.5, 15.0, "StoreStaff", tables_info["StoreStaff"]["cols"], tables_info["StoreStaff"]["pk"])
draw_vertical_table(20.5, 11.0, "StoreMaterials", tables_info["StoreMaterials"]["cols"], tables_info["StoreMaterials"]["pk"])
draw_vertical_table(20.5, 7.5, "RecipeStandards", tables_info["RecipeStandards"]["cols"], tables_info["RecipeStandards"]["pk"])
draw_vertical_table(20.5, 4.0, "RawMaterials", tables_info["RawMaterials"]["cols"], tables_info["RawMaterials"]["pk"])

def draw_fk_arrow(from_table, from_col, to_table, to_col, from_side="left", to_side="right", rad=0.0):
    p_from = col_coords[(from_table, from_col)][from_side]
    p_to = col_coords[(to_table, to_col)][to_side]
    
    con = ConnectionPatch(
        xyA=p_from, xyB=p_to,
        coordsA="data", coordsB="data",
        axesA=ax, axesB=ax,
        arrowstyle="-|>",
        connectionstyle=f"arc3,rad={rad}",
        color=LINE_COLOR,
        lw=1.2,
        mutation_scale=10
    )
    ax.add_artist(con)

# Connecting Foreign Keys
draw_fk_arrow("MembershipAccounts", "CustomerId", "Customers", "CustomerId", "top", "bottom", rad=0.0)
draw_fk_arrow("MemberCampaigns", "MemberId", "MembershipAccounts", "MemberId", "left", "right", rad=0.1)
draw_fk_arrow("MemberCampaigns", "CampaignId", "PromotionCampaigns", "CampaignId", "left", "left", rad=-0.3)
draw_fk_arrow("DigitalOrders", "MemberId", "MembershipAccounts", "MemberId", "left", "right", rad=-0.1)
draw_fk_arrow("DigitalOrders", "ChannelId", "DigitalChannels", "ChannelId", "left", "right", rad=0.1)
draw_fk_arrow("OrderCampaigns", "OrderId", "DigitalOrders", "OrderId", "top", "bottom", rad=0.0)
draw_fk_arrow("OrderCampaigns", "CampaignId", "PromotionCampaigns", "CampaignId", "bottom", "top", rad=0.0)

draw_fk_arrow("OrderItems", "OrderId", "DigitalOrders", "OrderId", "left", "right", rad=0.1)
draw_fk_arrow("OrderItems", "ProductId", "Products", "ProductId", "right", "left", rad=0.0)

draw_fk_arrow("FulfilmentTasks", "OrderId", "DigitalOrders", "OrderId", "left", "right", rad=-0.1)
draw_fk_arrow("FulfilmentTasks", "StoreId", "Stores", "StoreId", "right", "left", rad=0.0)
draw_fk_arrow("FulfilmentTasks", "PartnerId", "DeliveryPartners", "PartnerId", "left", "left", rad=-0.3)

draw_fk_arrow("StoreStaff", "StoreId", "Stores", "StoreId", "left", "right", rad=0.1)
draw_fk_arrow("StoreMaterials", "StoreId", "Stores", "StoreId", "left", "right", rad=-0.1)
draw_fk_arrow("StoreMaterials", "MaterialId", "RawMaterials", "MaterialId", "right", "right", rad=0.3)

draw_fk_arrow("RecipeStandards", "ProductId", "Products", "ProductId", "left", "right", rad=0.0)
draw_fk_arrow("RecipeMaterials", "RecipeId", "RecipeStandards", "RecipeId", "right", "left", rad=-0.1)
draw_fk_arrow("RecipeMaterials", "MaterialId", "RawMaterials", "MaterialId", "right", "left", rad=0.1)
draw_fk_arrow("RawMaterials", "SupplierId", "Suppliers", "SupplierId", "left", "right", rad=0.0)

ax.text(12, 15.6, "Luckin Coffee Inc. Relational Database Schema Diagram", 
        ha="center", va="center", fontsize=18, fontweight="bold")
ax.text(12, 0.5, "Note: Underlined fields represent Primary Keys (PK). Arrows point from Foreign Keys (FK) to referenced Primary Keys.", 
        ha="center", va="center", fontsize=10, style="italic")

fig.tight_layout(pad=0.2)
fig.savefig(OUT, format="pdf", bbox_inches="tight")
print(f"Generated relational schema diagram at: {OUT}")
