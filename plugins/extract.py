import pandas as pd

def extract_sales(engine):
    query = "SELECT * FROM source_sales"
    df = pd.read_sql(query, engine)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df