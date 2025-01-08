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

## Algorithm overview

To process the input commands, I have developed 2 algorithms. 

The first algorithm ([`app/execute_commands_v1.py`](app/execute_commands_v1.py)), the algorithm uses a `set` to store the visited points `(x, y)`. Using a set is advantageous over a list because it automatically handles duplicates, ensuring each point is unique. The algorithm processes each command and its steps sequentially, resulting in a time complexity of `O(c * s)` and a space complexity of `O(c * s)`, where `c` is the number of commands and `s` is the average number of steps per command.

For the version 2 implementation ([`app/execute_commands_v2.py`](app/execute_commands_v2.py)), I created a class called `Line` to store visited locations as vertical and horizontal lines. The `Line` data structure has three properties: `constant`, `start`, and `end`. For example, a vertical line from `(0,0)` to `(0,4)` is represented as `Line(constant=0, start=0, end=4)`.

After creating lines for each command `(O(c))`, the overlapping lines are merged `(O(c log(c)))`, and the crossing positions (duplicated points) are calculated `(O(cˆ2))`. Finally, the total number of visited locations is determined by calculating the size of the final vertical and horizontal lines and subtracting the number of crossing points.

### Algorithms performances analysis

#### Time complexity

The time complexity of the V1 implementation is linear with respect to the total number of steps multiplied by the total number of commands in the input. In contrast, the V2 implementation has a quadratic time complexity relative to the number of commands. Given the problem constraints, where `0 ≤ number of commands ≤ 10000` and `0 < steps < 100000`, the maximum number of commands squared (10000²) is significantly lower than the maximum number of commands multiplied by the maximum number of steps `(10000 * 100000)`. Additionally, considering that in a realistic scenario the cleaning robot would likely operate in long lines, the V2 algorithm generally offers better performance.

I conducted a benchmark by writing performance tests that increase the number of commands and steps. These tests are available in the `/tests/performance_tests` directory. The test suite generates graphs of steps versus execution time, which are stored in the `/images` folder.

##### Realistic path
The graph demonstrates that in realistic scenarios, the V2 algorithm is significantly faster than V1. The test was limited to a maximum algorithm execution duration of 1 second. V1 could only complete a few executions before reaching this limit, whereas V2 was able to handle more executions within the same timeframe.
![Realistic Path Performance](images/plot_realistic_path.png)

##### Teeth Path

In contrast, for the "teeth" path scenario where the step size is always one and the number of lines is large, the V1 algorithm outperformed V2. This is because the number of commands significantly impacts the time complexity for V2, making the algorithm slower in such cases.
![Teeth Path Performance](images/plot_teeth_path.png)

#### Space complexity

The V1 algorithm saves all the visited points in memory. Considering the constraints, the maximum space used could be the maximum number of commands multiplied by the maximum number of steps `(10,000 * 100,000)`, where a tuple of integers is stored to represent each point. Therefore, considering an integer is 4 bytes, the maximum space used for the tuple (int, int) is 8 bytes. This results in a maximum space usage of `8 * 10,000 * 100,000 = 8,000,000,000 bytes` or approximately 8 GB.

In contrast, the V2 algorithm uses lines to store visited locations. The maximum number of lines is equal to the maximum number of commands `(10,000)`. Each line is represented by three integers (constant, start, end), resulting in a space usage of 12 bytes per line. Therefore, the maximum space used by the V2 algorithm is `12 * 10,000 = 120,000 bytes` or approximately 120 KB.

Thus, the V2 algorithm is significantly more space-efficient compared to the V1 algorithm.


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

