# Makefile for Robot Cleaning Service

.PHONY: up unit-tests integration-tests e2e-tests

build:
	docker-compose build

up:
	docker-compose up --build -d

test:
	docker exec -it robot-cleaning-service-app bash -c "PYTHONPATH=/ python -m unittest discover -s /app -p '*_test.py'"

integration-test:
	docker exec -it robot-cleaning-service-app bash -c "PYTHONPATH=/ python db_test.py"

e2e-test:
	docker exec -it robot-cleaning-service-app bash -c "PYTHONPATH=/ python e2e_test.py"

test-coverage:
	docker exec -i robot-cleaning-service-app bash -c "PYTHONPATH=/ coverage run --source=/app -m unittest discover -s /app -p '*_test.py' && coverage report && coverage html"