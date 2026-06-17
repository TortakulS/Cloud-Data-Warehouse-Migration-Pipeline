from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,                    
    'retry_delay': timedelta(minutes=5), 
}

with DAG(
    dag_id='postgres_to_bigquery_pipeline', 
    default_args=default_args,
    description='Intermediate ETL: Postgres to Google BigQuery',
    schedule_interval=None,            
    start_date=datetime(2026, 1, 1),    
    catchup=False,
    tags=['intermediate', 'etl'],
) as dag:

    extract_task = BashOperator(
        task_id='extract_data',
        bash_command='python /opt/airflow/scripts/extract.py', 
    )
    transform_task = BashOperator(
        task_id='transform_data',
        bash_command='python /opt/airflow/scripts/transform.py',
    )

    load_task = BashOperator(
        task_id='load_data',
        bash_command='python /opt/airflow/scripts/load.py',
    )

    extract_task >> transform_task >> load_task