#!/bin/bash

# Создание БД
sleep 10
airflow db init
sleep 15

airflow users create \
    --username airflow \
    --firstname airflow \
    --lastname airflow \
    --role Admin \
    --email admin@example.org \
    -p 12345678

# Запуск шедулера и вебсервера
airflow scheduler & airflow webserver