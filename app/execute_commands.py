from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
import time
import logging
from typing import List, Tuple, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RobotCleaningService")


class Line:
    def __init__(self, constant: int, start: int, end: int):
        self.constant = constant
        self.start = start
        self.end = end

    def __lt__(self, other):
        return (self.constant, self.start, self.end) < (
            other.constant,
            other.start,
            other.end,
        )

    def __eq__(self, other):
        if isinstance(other, Line):
            return (
                self.constant == other.constant
                and self.start == other.start
                and self.end == other.end
            )
        return False

    def __repr__(self):
        return f"Line(constant={self.constant}, start={self.start}, end={self.end})"


def create_lines(
    x: int, y: int, commands: List[Dict[str, int]]
) -> Tuple[List[Line], List[Line]]:
    """
    Generates horizontal and vertical lines based on a starting point and a list of movement commands.

    Returns:
        Tuple[List[Line], List[Line]]: A tuple containing two lists of Line objects. The first list contains
                                       horizontal lines, and the second list contains vertical lines.
    """

    horizontal_lines = []
    vertical_lines = []
    current_x, current_y = x, y

    for command in commands:  # O(n)
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


def merge_segments(lines: List[Line]) -> List[Line]:
    """
    Merges overlapping or contiguous line segments with the same constant value.

    Returns:
        List[Line]: A list of merged Line objects.
    """
    lines.sort()  # O(nlogn)
    merged_lines = []

    for line in lines:  # O(n)
        if not merged_lines:
            merged_lines.append(line)
            continue

        last_line = merged_lines[-1]
        if last_line.constant == line.constant:
            if (line.start <= last_line.end and last_line.end <= line.end) or (
                last_line.start <= line.end and line.end <= last_line.end
            ):
                new_line = Line(
                    line.constant,
                    min(last_line.start, line.start),
                    max(last_line.end, line.end),
                )
                merged_lines[-1] = new_line
            else:
                merged_lines.append(line)
        else:
            merged_lines.append(line)

    return merged_lines


def count_points(lines: List[Line]) -> int:
    count = 0
    for line in lines:
        count += line.end - line.start + 1
    return count


def calculate_crossings(
    vertical_lines: List[Line], horizontal_lines: List[Line]
) -> int:
    count = 0
    for v_line in vertical_lines:  # O(nˆ2)
        for h_line in horizontal_lines:
            if (v_line.start <= h_line.constant <= v_line.end) and (
                h_line.start <= v_line.constant <= h_line.end
            ):
                count += 1
    return count


def execute_commands_v2(
    commands: List[Dict[str, int]], x: int, y: int
) -> Tuple[int, float]:
    """
    Algorithm V2:
    Executes a series of commands to move a robot and calculates the number of unique points visited.
    time complexity: O(nlogn)
    space complexity: O(n)

    Args:
        commands (List[Dict[str, int]]): A list of commands where each command is a dictionary
                                         with direction and distance.
        x (int): The starting x-coordinate of the robot.
        y (int): The starting y-coordinate of the robot.

    Returns:
        Tuple[int, float]: A tuple containing the number of unique points visited and the
                           duration of the execution in seconds.
    """

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


def execute_commands_v1(
    commands: List[Dict[str, int]], x: int, y: int
) -> Tuple[int, float]:
    """
    Algorithm V1:
    Executes a series of movement commands starting from a given position and
    returns the number of unique cells visited and the duration of execution.
    Time Complexity: O(commands x steps)
    Space Complexity: O(commands x steps)

    Args:
        commands (List[Dict[str, int]]): A list of movement commands where each
            command is a dictionary with 'direction' (str) and 'steps' (int).
        x (int): The starting x-coordinate.
        y (int): The starting y-coordinate.

    Returns:
        Tuple[int, float]: A tuple containing the number of unique cells visited
        and the duration of execution in seconds.
    """

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
