Порядок действий

1. Создать инфраструктуру
    ```bash
    bash create_infra.sh
    ```

2. Заполнить креды в коде из файла airflow-sa.json
   
3. Обучить модель
    ```bash
    python3 train.py
    ```

4. Загрузить данные для инференса и модель в S3
    ```bash
    bash upload.sh
    ```

5. Запустить локальный Airflow
    ```bash
    docker-compose up -d --build
    ```

6. Выбрать DAG в UI и нажать Trigger DAG
   ```bash
   http:\\localhost:8001\
   
   # user
   airflow

   # pass
   12345678
   ```