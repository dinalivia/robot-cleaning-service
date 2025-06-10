from flask import request, jsonify
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from app import create_app, db
from app.execute_commands_v2 import execute_commands_v2
import logging

from app.db_queries import ExecutionQueryService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RobotCleaningService")

app = create_app(db)
db_service = ExecutionQueryService(db)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/robot-cleaning-service/get-last-executions", methods=["GET"])
def get_last_executions():
    # for testing purposes
    executions = db_service.get_last_executions()
    return jsonify(
        [
            {
                "result": execution.result,
                "commands": execution.commands,
                "duration": execution.duration,
                "timestamp": execution.timestamp,
            }
            for execution in executions
        ]
    )


@app.route("/robot-cleaning-service/enter-path", methods=["POST"])
def enter_path():
    try:
        inputs = EnterPathInput(request)
        if not inputs.validate():
            logger.error("Input validation failed")
            return jsonify({"error": inputs.errors}), 400

        data = request.get_json()
        start = data["start"]
        commands = data["commmands"]

        result, duration = execute_commands_v2(commands, start["x"], start["y"])

        execution = db_service.add_execution(len(commands), result, duration)

        db.session.add(execution)
        db.session.commit()

        logger.info(f"Successfully executed {len(commands)} commands")

        return (
            jsonify(
                {
                    "result": result,
                    "commands": len(commands),
                    "duration": duration,
                    "timestamp": execution.timestamp,
                }
            ),
            201,
        )
    except MemoryError:
        logger.critical("MemoryError occurred")
        return jsonify({"error": "Internal server error"}), 500
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "Internal server error"}), 500


class EnterPathInput(Inputs):
    json = [
        JsonSchema(
            schema={
                "type": "object",
                "properties": {
                    "start": {
                        "type": "object",
                        "properties": {
                            "x": {
                                "type": "integer",
                                "minimum": -100000,
                                "maximum": 100000,
                            },
                            "y": {
                                "type": "integer",
                                "minimum": -100000,
                                "maximum": 100000,
                            },
                        },
                        "required": ["x", "y"],
                    },
                    "commmands": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "direction": {
                                    "type": "string",
                                    "enum": ["north", "south", "east", "west"],
                                },
                                "steps": {"type": "integer", "minimum": 0},
                            },
                            "required": ["direction", "steps"],
                        },
                        "maxItems": 10000,
                    },
                },
                "required": ["start", "commmands"],
            }
        )
    ]
