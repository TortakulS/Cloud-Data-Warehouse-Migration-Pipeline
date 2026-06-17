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

    print("SUCCESS! ")
