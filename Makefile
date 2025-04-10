down:
	docker-compose down

build:
	docker-compose build

up:
	docker-compose down
	docker-compose up -d --build

execute:
	docker exec -it airflow bash

create-infra:
	bash scripts/create-infra.sh

upload-data:
	bash scripts/upload-data.sh

upload-model:
	bash scripts/upload-model.sh

train:
	python3 src/train.py
