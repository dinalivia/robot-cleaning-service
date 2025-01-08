# Makefile for Robot Cleaning Service

.PHONY: build up up-ci down tests unit-test integration-test e2e-test performance_test test-coverage

build:
	docker compose build

up:
	docker compose up --build

down:
	docker compose down --volumes

up-ci:
	docker compose up --build -d

test:
	docker exec -it robot-cleaning-service-app bash -c "PYTHONPATH=/ python -m unittest discover -s /app/tests -p '*_test.py'"

unit-test:
	python -m unittest app/tests/execute_commands_v1_test.py app/tests/execute_commands_v2_test.py app/tests/enter_path_test.py

integration-test:
	docker exec -it robot-cleaning-service-app bash -c "PYTHONPATH=/ python tests/db_test.py"

e2e-test:
	docker exec -it robot-cleaning-service-app bash -c "PYTHONPATH=/ python tests/e2e_test.py"

performance-test:
	python -m unittest app/tests/performance_tests/performance_test.py

test-coverage:
	docker exec -i robot-cleaning-service-app bash -c "PYTHONPATH=/ coverage run --source=/app -m unittest discover -s /app/tests -p '*_test.py' && coverage report && coverage html"