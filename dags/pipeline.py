from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))

from Functions.connections import (
    load_json_config
)
#MAC ISSUE
os.environ['NO_PROXY'] = '*'

with DAG(
    dag_id="blue_harvest_marvel",
    schedule_interval=None,
    start_date=datetime(2025, 1, 10),
    catchup=False,
) as dag:

    load_json = PythonOperator(
        task_id="read_json",
        python_callable=load_json_config
    )

    load_json
