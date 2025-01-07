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

## Algorithm performance

To process the input commands, I have developed 2 algorithms. 

For the first algorithm (execute_commands_v1) I chose to use a `set` as the data structure to save the visited points, and the algorithm loops through each command and step given in the input. The time complexity of O(c*s), and space complexity of O(c*s), where `c` is the number of Commands and `s` the average number of steps per command. 

For the version 2 of this implementation (execute_commands_v2), I created a class called `Line`, to save the visited locations as vertical and horizontal lines. The Line data scruture has 3 properties: a `constant`, a `start` and an `end`. (TODO: explain properties)
After creating the lines for each command, the overlapping lines are merged and and the crossing positions (duplicated points) are calculated. Finally, the total amount of visited locations is returned by calculating the size of the final vertical and horizontal lines and subtracting the amount of crossing points.

V2 é quadrádico ao numero de comandos 
V1 é linear ao numero total de passos

o quadradico do numero `max de comandos` é menor do que o num `max de comandos x max numero de passos` em uma ordem de grandeza.

TODO:
vantagem: linhas ao inves pontos para armazenados em memorias. num max Linhas (10k) = num max de commandos, já o num max de pontos (V1) é no max o max do num passos (100k) X num max do comandos(10k). 
- linhas sao ordenadas, isso diminui a complexidade na hora de mergear os segments (remove overlappings)

Casos extremos:
- prox ao valor max dos steps, o algoritmo V2 tem uma clara performance superior ao algoritmo um
- caso o numero de steps seja prox ou igual 1 e 


<!-- The advantage of using lines instead of unique points (as in V1) is that I can process the distances (steps) and avoid a nested loop to process the input, reducing the time and space complexity on the average execution. -->

To analyse both algorithms performance, I created a small benchmark 


## Setting Up the Project 

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
   pip install -r requirements.txt
   ```

5. Run the Flask application locally:
   ```bash
   export FLASK_APP=main.py
   export FLASK_ENV=development
   flask run
   ```
   For Windows:
   ```bash
   set FLASK_APP=main.py
   set FLASK_ENV=development
   flask run
   ```

## Managing Dependencies with Poetry

To ensure that dependencies run correctly on another machine, we recommend using [Poetry](https://python-poetry.org/), a simple and lightweight package manager for Python.

1. **Install Poetry**:
   Follow the instructions on the [Poetry installation page](https://python-poetry.org/docs/#installation) to install Poetry on your system.

2. **Initialize Poetry in the Project**:
   ```bash
   poetry init
   ```

3. **Add Project Dependencies**:
   ```bash
   poetry add $(cat requirements.txt)
   ```

4. **Install Dependencies**:
   ```bash
   poetry install
   ```

5. **Activate the Virtual Environment**:
   ```bash
   poetry shell
   ```

By using Poetry, you can ensure that all dependencies are managed consistently across different environments.

5. Build the Docker containers:
   ```bash
   make build
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
- **Code performance analysis**: run e2e tests locally to check the code time complexity. The test suite plots a graph of commands x execution time. The graph is stored at `app/duration_vs_commands_steps.png`


## Design of the system

## Future expansion 
what i'd have done with more time
