# OTUS. Batch Mode. Airflow Local


Порядок действий

1. Создать инфраструктуру
    ```bash
    make create-infra
    ```
2. Обучить модель
    ```bash
    make train
    ```
3. Загрузить данные для инференса и модель в S3
    ```bash
    make upload-data
    make upload-model
    ```
4. Запустить локальный Airflow
    ```bash
    make up
    ```
5. Добавить variables.json в UI Airflow:
    ```bash
    http:\\localhost:8001\
   
    # user
    airflow

    # pass
    12345678
    ```
7. Выбрать нужный DAG в UI и нажать Trigger DAG
