# Robot Cleaning Service

## Goal of the Project
The Robot Cleaning Service is an API that processes cleaning commands for a robot. It tracks the robot's movements, calculates the number of unique positions visited, and stores execution data in a database for analysis. The service is designed to be scalable, efficient, and ready for deployment in serverless environments like AWS Lambda.

## Requirements
To run this project, ensure you have the following:

- **Python 3.9 or later**
- **Docker** (with Docker Compose)
- **pip** for Python package management

## Quick start the project - with docker containers

To run the service:

1. Clone the repository:
   ```bash
   git clone git@github.com:dinalivia/robot-cleaning-service.git
   cd robot-cleaning-service
   ```

2. **Run with Docker Compose**:
   ```bash
   make up
   ```

3. **Access the API**:
   - API Base URL: `http://localhost:5000`
   - Example Endpoint: `POST /tibber-developer-test/enter-path`

. **Send a Sample Request**:
   Use a tool like `curl`, Postman, or any HTTP client to test the service:
   ```bash
   curl -X POST http://localhost:5000/tibber-developer-test/enter-path \
   -H "Content-Type: application/json" \
   -d '{
       "start": {"x": 0, "y": 0},
       "commmands": [
           {"direction": "north", "steps": 1},
           {"direction": "east", "steps": 1},
           {"direction": "south", "steps": 1},
           {"direction": "west", "steps": 1}
       ]
   }'
   ```
## Design of the system
The system is designed with a modular approach. The command execution logic, data storage, and API handling are separated into different components for better maintainability and scalability. The database used is PostgreSQL, and the application is built with Flask for the web framework. The command execution algorithms are implemented in separate Python files, ensuring a clear separation of concerns and ease of testing.

## Algorithm Overview
For a detailed analysis of the solution idealization and code performance, check the [SOLUTION_ANALYSIS.md](./SOLUTION_ANALYSIS.md).

## Setting Up the Project locally

1. Clone the repository:
   ```bash
   git clone git@github.com:dinalivia/robot-cleaning-service.git
   cd robot-cleaning-service
   ```

2. Set Up a Python Virtual Environment (Optional but Recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\\Scripts\\activate   # For Windows
   ```

3. Create a `.env` file for environment variables (optional but recommended):
   ```bash
   echo "DATABASE_URI=postgresql://user:password@localhost:5432/robot_service" > .env
   ```

4. Install dependencies (if running locally):
   ```bash
   pip install -r requirements-dev.txt
   ```

5. Run the Flask application locally:
   ```bash
   export FLASK_APP=main.py
   export FLASK_ENV=development
   flask db upgrade && flask run --host=0.0.0.0 --port=5000
   ```
   For Windows:
   ```bash
   set FLASK_APP=main.py
   set FLASK_ENV=development
   flask db upgrade && flask run --host=0.0.0.0 --port=5000
   ```


## Running Tests
The project is configured with unit, integration, and end-to-end (E2E) tests. Follow the steps below to run them:

### 1. All Tests 
Run unit, integration and e2e tests using the following command:
```bash
make test
```

### 2. Integration Tests
Run integration tests only with:
```bash
make integration-tests
```

### 3. End-to-End Tests
Run E2E tests only with:
```bash
make e2e-tests
```

### 4. Check code coverage
Run:
```bash
make test-coverage
```

## Additional Information
- **Logs**: The service uses structured logging for better debugging.
- **CI**: Automated tests are run using GitHub Actions.
- **Code performance analysis**: run performance tests locally to check the code time complexity. The test suite plots graphs of steps x execution time. The graphs are stored at `/images` folder

## Future Expansion

- **Dependency Management**: Utilize Poetry or another Python package manager for consistent dependency management. Split production and development dependencies into separate `requirements.txt` files for better environment management.
- **Cloud Deployment**: Deploy the application on cloud platforms such as AWS for scalability and reliability. Integrate with CI/CD pipelines for automated testing and deployment.
- **Monitoring and Analysis**: Integrate Datadog for comprehensive service monitoring and analysis. Implement a web-based dashboard for real-time monitoring and control of the cleaning robots.
- **Algorithm Optimization**: Explore further optimizations for the V2 implementation to enhance performance.
- **Testing Environment**: Create a separate database instance solely for testing end-to-end and integration tests.

