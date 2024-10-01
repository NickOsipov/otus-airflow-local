"""
Module for testing DAG
"""

from datetime import datetime, timedelta
import os
import sqlite3
import pandas as pd

from airflow import DAG
# from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator


os.makedirs("/root/data", exist_ok=True)
CON = sqlite3.connect('/root/data/example.db')

# 2024-03-04 13:00:00
start_date = datetime(2024, 3, 4, 16, 0, 0)


def extract_data(url, tmp_file) -> pd.DataFrame:
    """
    Not empty
    """
    pd.read_csv(url).to_csv(tmp_file) # Изменение to_csv


def transform_data(group, agreg, tmp_file, tmp_agg_file) -> pd.DataFrame:
    """
    Not empty
    """
    data = pd.read_csv(tmp_file) # Изменение read_csv
    data.groupby(group).agg(agreg).reset_index().to_csv(tmp_agg_file) # Изменение to_csv


def load_data(tmp_file, table_name, conn=CON) -> None:
    """
    Not empty
    """
    data = pd.read_csv(tmp_file)# Изменение read_csv
    data["insert_time"] = pd.to_datetime("now")
    data.to_sql(table_name, conn, if_exists='replace', index=False)


with DAG(
    dag_id='dag_check_start_date',
    default_args={'owner': 'airflow'},
    schedule_interval="0,15,30,45 * * * *",
    start_date=start_date,
    catchup=False
) as dag:

    extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        op_kwargs={
            'url': 'https://raw.githubusercontent.com/NickOsipov/'
                   'small_data_examples/main/data.csv',
            'tmp_file': '/tmp/file.csv'},
        dag=dag
    )

    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        dag=dag,
        op_kwargs={
            'tmp_file': '/tmp/file.csv',
            'tmp_agg_file': '/tmp/file_agg.csv',
            'group': ['A', 'B', 'C'],
            'agreg': {"D": sum}}
    )

    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        dag=dag,
        op_kwargs={
            'tmp_file': '/tmp/file.csv',
            'table_name': 'dag_testing_table'
        }
    )

    extract_data >> transform_data >> load_data
