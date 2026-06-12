import re

with open("/Users/cccsh/Desktop/EA_Class/Seminar5/make_schema_diagram.py", "r") as f:
    content = f.read()

new_draw_table = """
def draw_table(x, y, table_name, columns, pk_indices, num_rows=NUM_ROWS, data=None):
    if data is None: data = []
    n_cols = len(columns)
    table_w = n_cols * CELL_W
    table_h = (num_rows + 1) * CELL_H
    
    table_corners[table_name] = (x, y)
    
    ax.text(x, y + 0.12, table_name, ha="left", va="bottom", fontsize=10, fontweight="bold", color="black")
    
    for i, col in enumerate(columns):
        cx = x + i * CELL_W
        cy = y - CELL_H
        rect = Rectangle((cx, cy), CELL_W, CELL_H, facecolor=RED_HEADER, edgecolor="black", linewidth=0.5)
        ax.add_patch(rect)
        
        is_pk = i in pk_indices
        font_weight = "bold" if is_pk else "normal"
        ax.text(cx + CELL_W/2, cy + CELL_H/2, col, color=TEXT_COLOR, 
                ha="center", va="center", fontsize=7.2, fontweight=font_weight)
        
        if is_pk:
            ax.plot([cx + 0.08, cx + CELL_W - 0.08], [cy + 0.04, cy + 0.04], color=TEXT_COLOR, lw=0.8)
            
        col_coords[(table_name, col)] = {
            "top": (cx + CELL_W/2, y),
            "bottom": (cx + CELL_W/2, cy),
            "left": (cx, cy + CELL_H/2),
            "right": (cx + CELL_W, cy + CELL_H/2),
            "center": (cx + CELL_W/2, cy + CELL_H/2)
        }
        
    for r in range(num_rows):
        ry = y - (r + 2) * CELL_H
        row_data = data[r] if r < len(data) else []
        for i in range(n_cols):
            cx = x + i * CELL_W
            rect = Rectangle((cx, ry), CELL_W, CELL_H, facecolor="white", edgecolor=BORDER_COLOR, linewidth=0.3)
            ax.add_patch(rect)
            
            cell_text = str(row_data[i]) if i < len(row_data) else ""
            if cell_text:
                ax.text(cx + CELL_W/2, ry + CELL_H/2, cell_text, color="black",
                        ha="center", va="center", fontsize=6)
            
    return table_w, table_h
"""
content = re.sub(r'def draw_table\(.*?return table_w, table_h', new_draw_table.strip(), content, flags=re.DOTALL)

replacements = {
    '"Customers": {': '"Customers": {\n        "data": [["C101", "White-collar", "BJ", "25-34"], ["C102", "Student", "SH", "18-24"]],',
    '"MembershipAccounts": {': '"MembershipAccounts": {\n        "data": [["M901", "C101", "1500", "50", "Gold", "Active"], ["M902", "C102", "300", "15", "Silver", "Active"]],',
    '"DigitalChannels": {': '"DigitalChannels": {\n        "data": [["CH1", "App", "iOS", "v3.1"], ["CH2", "WeChat", "Android", "v2.0"]],',
    '"PromotionCampaigns": {': '"PromotionCampaigns": {\n        "data": [["P01", "NewUser", "Students", "30d", "15.0"], ["P02", "BOGO", "All", "7d", "20.0"]],',
    '"MemberCampaigns": {': '"MemberCampaigns": {\n        "data": [["M901", "P02", "06-01", "Used"], ["M902", "P01", "06-10", "Active"]],',
    '"DigitalOrders": {': '"DigitalOrders": {\n        "data": [["O501", "M901", "CH1", "Delivery", "WeChatPay", "Done", "35.0", "5.0", "06-12", "08:30"], ["O502", "M902", "CH2", "Pickup", "Alipay", "Queue", "15.0", "0.0", "06-12", "09:15"]],',
    '"OrderCampaigns": {': '"OrderCampaigns": {\n        "data": [["O501", "P02", "20.0"], ["O502", "P01", "15.0"]],',
    '"OrderItems": {': '"OrderItems": {\n        "data": [["O501", "1", "PR1", "1", "Half Sugar", "20.0", "35.0"], ["O502", "1", "PR2", "1", "Standard", "15.0", "15.0"]],',
    '"Products": {': '"Products": {\n        "data": [["PR1", "Coconut Latte", "Coffee", "Summer", "60%", "14.0"], ["PR2", "Americano", "Coffee", "All", "75%", "5.0"]],',
    '"RecipeStandards": {': '"RecipeStandards": {\n        "data": [["R101", "PR1", "v1.2", "Active", "14.0", "0.5%"], ["R102", "PR2", "v1.0", "Active", "5.0", "0.1%"]],',
    '"RecipeMaterials": {': '"RecipeMaterials": {\n        "data": [["R101", "RM1", "18g"], ["R101", "RM2", "200ml"]],',
    '"RawMaterials": {': '"RawMaterials": {\n        "data": [["RM1", "S01", "Coffee Beans", "Bean", "Yunnan", "OK", "5000"], ["RM2", "S02", "Coconut Milk", "Dairy", "Hainan", "OK", "2000"]],',
    '"Suppliers": {': '"Suppliers": {\n        "data": [["S01", "Yunnan Farm", "Farm", "3d"], ["S02", "Hainan Dairy", "Factory", "2d"]],',
    '"Stores": {': '"Stores": {\n        "data": [["ST01", "Tech Park", "Self", "Tier1", "Office", "50k", "15k"], ["ST02", "Uni Mall", "Partner", "Tier2", "Mall", "30k", "8k"]],',
    '"StoreStaff": {': '"StoreStaff": {\n        "data": [["SF1", "ST01", "Alice", "Manager", "Done", "40", "8k", "High"], ["SF2", "ST02", "Bob", "Barista", "Done", "35", "5k", "Med"]],',
    '"StoreMaterials": {': '"StoreMaterials": {\n        "data": [["ST01", "RM1", "50kg", "0%"], ["ST02", "RM2", "20L", "2%"]],',
    '"FulfilmentTasks": {': '"FulfilmentTasks": {\n        "data": [["T801", "O501", "ST01", "D01", "Delivery", "120s", "300s", "99%", "Handed"], ["T802", "O502", "ST02", "None", "Pickup", "90s", "60s", "100%", "Ready"]],',
    '"DeliveryPartners": {': '"DeliveryPartners": {\n        "data": [["D01", "SF Express", "Logistics", "CBD", "5.0", "0.1%"], ["D02", "Meituan", "O2O", "Campus", "4.5", "0.5%"]],'
}

for k, v in replacements.items():
    content = content.replace(k, v)

content = re.sub(r'draw_table\(([^,]+), ([^,]+), "([^"]+)", tables_info\["([^"]+)"\]\["cols"\], tables_info\["([^"]+)"\]\["pk"\]\)', 
                 r'draw_table(\1, \2, "\3", tables_info["\4"]["cols"], tables_info["\5"]["pk"], data=tables_info["\3"].get("data", []))', content)

with open("/Users/cccsh/Desktop/EA_Class/Seminar5/make_schema_diagram.py", "w") as f:
    f.write(content)
print("make_schema_diagram.py patched successfully.")
