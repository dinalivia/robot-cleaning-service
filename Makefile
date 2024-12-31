# Makefile for Robot Cleaning Service

.PHONY: up unit-tests integration-tests e2e-tests

build:
	docker-compose build

up:
	docker-compose up --build

unit-tests:
	docker exec -it $$(docker ps -qf "name=robot_cleaning_service-app-1") bash -c "PYTHONPATH=/ python -m unittest discover -s /app -p '*_test.py'"

integration-tests:
	docker exec -it $$(docker ps -qf "name=robot_cleaning_service-app-1") bash -c "PYTHONPATH=/ python db_test.py"

e2e-tests:
	docker exec -it $$(docker ps -qf "name=robot_cleaning_service-app-1") bash -c "PYTHONPATH=/ python e2e_test.py"

