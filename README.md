# Robot Cleaning Service

## Goal of the Project
The Robot Cleaning Service is an API that processes cleaning commands for a robot. It tracks the robot's movements, calculates the number of unique positions visited, and stores execution data in a database for analysis. The service is designed to be scalable, efficient, and ready for deployment in serverless environments like AWS Lambda.

## Requirements
To run this project, ensure you have the following:

- **Python 3.9 or later**
- **Docker** (with Docker Compose)
- **pip** for Python package management

## Setting Up the Project

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd robot-cleaning-service
   ```

2. Create a `.env` file for environment variables (optional but recommended):
   ```bash
   echo "DATABASE_URI=postgresql://user:password@localhost:5432/robot_service" > .env
   ```

3. Install dependencies (if running locally):
   ```bash
   pip install -r requirements.txt
   ```

4. Build the Docker containers:
   ```bash
   docker-compose build
   ```

## Running the Project

To start the service:

1. **Run with Docker Compose**:
   ```bash
   docker-compose up
   ```

2. **Access the API**:
   - API Base URL: `http://localhost:5000`
   - Example Endpoint: `POST /tibber-developer-test/enter-path`

3. **Send a Sample Request**:
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

## Running Tests
The project is configured with unit, integration, and end-to-end (E2E) tests. Follow the steps below to run them:

### 1. Unit Tests
Run unit tests using the following command:
```bash
make unit-tests
```

### 2. Integration Tests
Run integration tests with:
```bash
make integration-tests
```

### 3. End-to-End Tests
Run E2E tests with:
```bash
make e2e-tests
```

## Additional Information
- **Logs**: The service uses structured logging for better debugging.
- **Code Coverage**: Code coverage is tracked during unit tests and can be checked via `coverage report`.
- **Deployment**: This service is ready for deployment in serverless environments like AWS Lambda.

Feel free to contribute or raise issues if you encounter any problems!
