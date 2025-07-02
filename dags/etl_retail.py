from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import pandas as pd
import io
import os

# ── Shared path dalam container (volume mounted) ─────────────────
SHARED_DIR = "/opt/airflow/dags"
EXTRACT_CSV = os.path.join(SHARED_DIR, "retail_extract.csv")
TRANSFORM_CSV = os.path.join(SHARED_DIR, "retail_transformed.csv")

default_args = {
    "owner": "dewi",
    "start_date": datetime(2024, 1, 1),
}

# ── ETL Functions ────────────────────────────────────────────────
def extract_data():
    hook = PostgresHook(postgres_conn_id="pg_src")
    df = hook.get_pandas_df("SELECT * FROM retail_raw LIMIT 1000;")
    df.to_csv(EXTRACT_CSV, index=False)
    print(f"✅ Extracted {len(df)} rows → {EXTRACT_CSV}")

def transform_data():
    df = pd.read_csv(EXTRACT_CSV)

    # Pastikan nama kolom lowercase karena hasil dari PostgreSQL biasanya begitu
    df.columns = [col.lower() for col in df.columns]

    # Hitung TotalPrice dan drop missing values
    df["totalprice"] = df["quantity"] * df["unitprice"]
    df_clean = df.dropna()

    df_clean.to_csv(TRANSFORM_CSV, index=False)
    print(f"✅ Transformed {len(df_clean)} rows → {TRANSFORM_CSV}")

def load_data():
    hook = PostgresHook(postgres_conn_id="pg_src")
    df = pd.read_csv(TRANSFORM_CSV)

    create_sql = """
    CREATE TABLE IF NOT EXISTS retail_mart (
        InvoiceNo   TEXT,
        StockCode   TEXT,
        Description TEXT,
        Quantity    INTEGER,
        InvoiceDate TIMESTAMP,
        UnitPrice   NUMERIC,
        CustomerID  TEXT,
        Country     TEXT,
        TotalPrice  NUMERIC
    );
    """
    hook.run(create_sql)

    conn = hook.get_conn()
    cursor = conn.cursor()

    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    cursor.copy_from(output, "retail_mart", null="")
    conn.commit()
    print(f"✅ Loaded {len(df)} rows into retail_mart")

# ── DAG Definition ───────────────────────────────────────────────
with DAG(
    dag_id="etl_retail_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["retail", "etl", "postgres"],
) as dag:

    t_extract = PythonOperator(
        task_id="extract",
        python_callable=extract_data
    )

    t_transform = PythonOperator(
        task_id="transform",
        python_callable=transform_data
    )

    t_load = PythonOperator(
        task_id="load",
        python_callable=load_data
    )

    t_extract >> t_transform >> t_load
