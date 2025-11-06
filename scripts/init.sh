#!/bin/bash

# Создание БД
sleep 10
airflow db init
sleep 15

airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Запуск шедулера и вебсервера
airflow scheduler & airflow webserver
