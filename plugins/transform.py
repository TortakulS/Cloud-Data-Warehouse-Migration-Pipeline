import pandas as pd

def transform_sales(data):
    # ตรวจสอบค่าว่าง
    print("Missing values count:\n", data.isnull().sum())
    data = data.dropna(subset=['order_id'])
    
    # 1. คำนวณยอดรวม 
    data["total_amount"] = data["quantity"] * data["price"]
    
    # 2. หาประเภทสินค้าขายดี
    top_products = (
        data.groupby("product_name")["quantity"]
        .sum()
        .reset_index(name="total_quantity")
        .sort_values(by="total_quantity", ascending=False)
    )
    
    # 3. หาประเภทสินค้าที่ทำรายได้สูงสุด
    top_revenue = (
        data.groupby("product_name")["total_amount"]
        .sum()
        .reset_index(name="total_revenue")
        .sort_values(by="total_revenue", ascending=False)
    )
    
    # 4. แปลงค่าเฉลี่ยยอดซื้อให้กลายเป็น DataFrame
    order_total = (
        data.groupby("order_id")["total_amount"]
        .sum()
        .reset_index(name="order_total")
    )
    aov_value = order_total["order_total"].mean()
    aov = pd.DataFrame([{"average_order_value": aov_value}]) # เปลี่ยนเป็น DataFrame 1 แถว
    
    # 5. ยอดคำสั่งซื้อรายวัน
    orders_per_day = (
        data.groupby(data["order_date"].dt.date)["order_id"]
        .nunique()
        .reset_index(name="orders_per_day")
    )
    
    # 6. ยอดคำสั่งซื้อรายเดือน
    orders_per_month = (
        data.groupby(data["order_date"].dt.to_period("M").astype(str))["order_id"]
        .nunique()
        .reset_index(name="orders_per_month")
    )
    
    # 7. ยอดขายรวมรายวัน
    daily_sales = (
        data.groupby(data["order_date"].dt.date)["total_amount"]
        .sum()
        .reset_index(name="daily_sales")
    )
    return {
        "top_products": top_products,
        "top_revenue": top_revenue,
        "aov": aov,
        "orders_per_day": orders_per_day,
        "orders_per_month": orders_per_month,
        "daily_sales": daily_sales
    }