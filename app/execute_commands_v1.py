import time
import logging
from typing import List, Tuple, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RobotCleaningService")


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
