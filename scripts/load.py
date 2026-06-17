import os
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("GCP_DATASET_ID")

def load_sales(metrics_dict):
    client = bigquery.Client(project=PROJECT_ID)
    for table_name, df_metrics in metrics_dict.items():
        full_table_path = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
        
        if "order_date" in df_metrics.columns:
            df_metrics["order_date"] = pd.to_datetime(df_metrics["order_date"])
            
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND"
        )
        try:
            # ยิงข้อมูลขึ้น BigQuery
            job = client.load_table_from_dataframe(df_metrics, full_table_path, job_config=job_config)
            job.result()  
            
        except Exception as table_error:
            print(f"เกิดข้อผิดพลาดตาราง {table_name}: {table_error}")

    print("SUCCESS!")
    
if __name__ == "__main__":
    import os
    metrics_list = [
        "top_products",
        "top_revenue",
        "aov",
        "orders_per_day",
        "orders_per_month",
        "daily_sales"
    ]
    collected_metrics_dict = {}
    for metric in metrics_list:
        file_path = f"/opt/airflow/scripts/sales_{metric}.csv"
        if os.path.exists(file_path):
            df_metric = pd.read_csv(file_path)

            table_name = f"summary_{metric}"
            collected_metrics_dict[table_name] = df_metric
            print(f"  -> เตรียมตาราง {table_name} เรียบร้อย")
        else:
            print(f"เตือนภัย: ไม่พบไฟล์ {file_path}")
    if collected_metrics_dict:
        print("กำลังส่งข้อมูลขึ้น Google BigQuery...")
        load_sales(collected_metrics_dict)  
        print("[SUCCESS] ข้อมูลทุกตารางขึ้น Google BigQuery สำเร็จเสร็จสิ้นแล้วครับน้า!!!")
    else:
        print("Error")
