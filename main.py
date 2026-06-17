import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

from scripts.extract import extract_sales
from scripts.transform import transform_sales
from scripts.load import load_sales

def sales_postgres():
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_string)
    data = extract_sales(engine)
    transform = transform_sales(data)
    load_sales(transform)

if __name__ == "__main__":
    sales_postgres()