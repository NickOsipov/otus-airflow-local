"""
Batch prediction pipeline
"""

import os
from io import BytesIO
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import pandas as pd
import joblib
import boto3
import tempfile

# Параметры подключения к Yandex Object Storage
ACCESS_KEY = '' # <-- Вставьте свой ключ
SECRET_KEY = '' # <-- Вставьте свой секреьныый ключ
BUCKET_NAME = '' # <-- Вставьте свой бакет
ENDPOINT_URL = 'https://storage.yandexcloud.net'


def get_s3_client():
    session = boto3.session.Session()
    return session.client(
        service_name='s3',
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'batch_prediction_pipeline',
    default_args=default_args,
    description='A batch prediction pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False
)

def load_data_from_storage(**kwargs):
    s3_client = get_s3_client()
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key='dataset.csv')
    data_buffer = BytesIO(response['Body'].read())
    df = pd.read_csv(data_buffer)
    return df.to_json()

def load_model_from_storage(**kwargs):
    s3_client = get_s3_client()
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key='model.joblib')
    model_buffer = BytesIO(response['Body'].read())
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.joblib') as temp_file:
        temp_file.write(model_buffer.getvalue())
        temp_file_path = temp_file.name
    
    return temp_file_path

def predict(**kwargs):
    ti = kwargs['ti']
    data_json = ti.xcom_pull(task_ids='load_data_task')
    df = pd.read_json(data_json)
    
    model_path = ti.xcom_pull(task_ids='load_model_task')
    model = joblib.load(model_path)
    
    predictions = model.predict(df)
    df['predictions'] = predictions
    
    os.remove(model_path)  # Удаляем временный файл
    
    return df.to_json()

def save_results_to_storage(**kwargs):
    ti = kwargs['ti']
    results_json = ti.xcom_pull(task_ids='make_predictions_task')
    df = pd.read_json(results_json)
    
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    
    s3_client = get_s3_client()
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key='predictions.csv',
        Body=buffer.getvalue()
    )

load_data_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data_from_storage,
    dag=dag,
)

load_model_task = PythonOperator(
    task_id='load_model_task',
    python_callable=load_model_from_storage,
    dag=dag,
)

predict_task = PythonOperator(
    task_id='make_predictions_task',
    python_callable=predict,
    dag=dag,
)

save_results_task = PythonOperator(
    task_id='save_results_task',
    python_callable=save_results_to_storage,
    dag=dag,
)

# pylint: disable=pointless-statement
[load_data_task, load_model_task] >> predict_task >> save_results_task
