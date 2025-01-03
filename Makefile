# Makefile for Robot Cleaning Service

.PHONY: build up tests integration-tests e2e-tests test-coverage

build:
	docker-compose build

up:
	docker-compose up --build

down:
	docker compose down --volumes

up-ci:
	docker-compose up --build -d

test:
	docker exec -it robot-cleaning-service-app bash -c "PYTHONPATH=/ python -m unittest discover -s /app/tests -p '*_test.py' $(ARGS)"

unit-test:
	docker exec -it robot-cleaning-service-app bash -c "PYTHONPATH=/ python tests/execute_commands_test.py tests/enter_path_test.py"

integration-test:
	docker exec -it robot-cleaning-service-app bash -c "PYTHONPATH=/ python tests/db_test.py"

e2e-test:
	docker exec -it robot-cleaning-service-app bash -c "PYTHONPATH=/ python tests/e2e_test.py"

performance_test:
	docker exec -it robot-cleaning-service-app bash -c "PYTHONPATH=/ python -m unittest discover -s /app/tests/performance_tests -p '*_test.py'"

test-coverage:
	docker exec -i robot-cleaning-service-app bash -c "PYTHONPATH=/ coverage run --source=/app -m unittest discover -s /app/tests -p '*_test.py' && coverage report && coverage html"