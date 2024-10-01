down:
	docker-compose down

build:
	docker-compose build

up:
	docker-compose down
	docker-compose up -d --build

execute:
	docker exec -it airflow bash