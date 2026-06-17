import pandas as pd

def extract_sales(engine):
    
    try:
        print(f"กำลังเชื่อมต่อไปยัง Postgres ที่โฮสต์: {engine}") 
        query = "SELECT * FROM source_sales"
        df = pd.read_sql(query, engine)
        df["order_date"] = pd.to_datetime(df["order_date"])
        print(f" ดึงข้อมูลสำเร็จ! พบข้อมูลทั้งหมด {len(df)} แถว") 

    except Exception as e:
        print(f"Error: {e}") 
        raise e 
    return df

if __name__ == "__main__":
    from sqlalchemy import create_engine
    import os
    from dotenv import load_dotenv
    load_dotenv()
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_string)

    df = extract_sales(engine)
    df.to_csv("/opt/airflow/scripts/sales_output.csv", index=False)