from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RobotCleaningService")


class Line:
    def __init__(self, constant, start, end):
        self.constant = constant
        self.start = start
        self.end = end

    def __lt__(self, other):
        return (self.constant, self.start, self.end) < (
            other.constant,
            other.start,
            other.end,
        )

    def __repr__(self):
        return f"Line(constant={self.constant}, start={self.start}, end={self.end})"


def create_lines(x, y, commands):
    horizontal_lines = []
    vertical_lines = []
    current_x, current_y = x, y

    for command in commands:
        direction = command["direction"]
        distance = command["steps"]

        if direction == "north":
            new_y = current_y + distance
            vertical_lines.append(Line(current_x, current_y, new_y))
            current_y = new_y
        elif direction == "south":
            new_y = current_y - distance
            vertical_lines.append(Line(current_x, new_y, current_y))
            current_y = new_y
        elif direction == "east":
            new_x = current_x + distance
            horizontal_lines.append(Line(current_y, current_x, new_x))
            current_x = new_x
        elif direction == "west":
            new_x = current_x - distance
            horizontal_lines.append(Line(current_y, new_x, current_x))
            current_x = new_x

    return horizontal_lines, vertical_lines


def merge_segments(lines):
    lines.sort()  # O(nlogn)
    normalized_lines = []

    for line in lines:  # O(n)
        if not normalized_lines:
            normalized_lines.append(line)
            continue

        last_line = normalized_lines[-1]
        if last_line.constant == line.constant:
            if (line.start <= last_line.end and last_line.end <= line.end) or (
                last_line.start <= line.end and line.end <= last_line.end
            ):
                new_line = Line(
                    line.constant,
                    min(last_line.start, line.start),
                    max(last_line.end, line.end),
                )
                normalized_lines[-1] = new_line
            else:
                normalized_lines.append(line)
        else:
            normalized_lines.append(line)

    return normalized_lines


def count_points(lines):
    count = 0
    for line in lines:
        count += line.end - line.start + 1
    return count


def calculate_crossings(vertical_lines, horizontal_lines):
    count = 0
    for v_line in vertical_lines:
        for h_line in horizontal_lines:
            if (v_line.start <= h_line.constant <= v_line.end) and (
                h_line.start <= v_line.constant <= h_line.end
            ):
                count += 1
    return count


def execute_commands_v2(commands, x, y):
    start_time = time.time()

    if not commands:
        return 1, time.time() - start_time

    # computes the segments
    horizontal_lines, vertical_lines = create_lines(x, y, commands)

    # merge segments
    normalized_horizontal_lines = merge_segments(horizontal_lines)
    normalized_vertical_lines = merge_segments(vertical_lines)

    # calculate number of points
    horizontal_points = count_points(normalized_horizontal_lines)
    vertical_points = count_points(normalized_vertical_lines)

    # detect intersections
    crossings = calculate_crossings(
        normalized_vertical_lines, normalized_horizontal_lines
    )
    # return the number of points and duration
    return (horizontal_points + vertical_points - crossings), time.time() - start_time


# explain my train of thought
# attempting to reduce the time complexity of the function because it's a web service and the time complexity
# would be O(commands x steps) which is not good
# it's a synchronous function and it's not good to have a function that takes a lot of time to execute
# I'm trying to reduce the time complexity of the function to O(nl) by creating lines and counting the points
# why use a set an not a list?
# because a set has O(1) complexity for the add operation


# split algorithm and controller


def execute_commands_v1(commands, x, y):
    visited = set()
    visited.add((x, y))

    start_time = time.time()

    for command in commands:  # O(commands x steps)
        direction = command["direction"]
        steps = command["steps"]

        for _ in range(steps):
            if direction == "north":
                y += 1
            elif direction == "south":
                y -= 1
            elif direction == "east":
                x += 1
            elif direction == "west":
                x -= 1
            visited.add((x, y))

    duration = time.time() - start_time
    logger.debug(f"Visited {len(visited)} unique cells in {duration} seconds")
    logger.debug(f"Visited cells: {visited}")
    return len(visited), duration


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
