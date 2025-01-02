import unittest
from app.main import execute_commands


class TestExecuteCommands(unittest.TestCase):
    def test_execute_commands_no_steps(self):
        commands = [
            {"direction": "north", "steps": 0},
        ]
        x, y = 0, 0
        result, duration = execute_commands(commands, x, y)
        self.assertEqual(result, 1)  # Only the start position

    def test_execute_commands_invalid_direction_is_ignored(self):
        commands = [
            {"direction": "invalid", "steps": 1},
        ]
        x, y = 0, 0
        result, duration = execute_commands(commands, x, y)
        self.assertEqual(result, 1)  # Only the start position
        self.assertIsNotNone(duration)

    def test_execute_commands_large_input(self):
        commands = [{"direction": "north", "steps": 1} for _ in range(10000)]
        x, y = 0, 0
        result, duration = execute_commands(commands, x, y)
        self.assertEqual(result, 10001)

    def test_execute_commands_successful_output(self):
        commands = [
            {"direction": "north", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "south", "steps": 1},
            {"direction": "west", "steps": 1},
        ]
        x, y = 0, 0
        result, duration = execute_commands(commands, x, y)
        self.assertEqual(result, 4)
        self.assertIsNotNone(duration)

    def test_execute_commands_straight_line_horizontal_case(self):
        commands = [
            {"direction": "east", "steps": 2},
            {"direction": "west", "steps": 2},
        ]
        x, y = 0, 0
        result, duration = execute_commands(commands, x, y)
        self.assertEqual(result, 3)
        self.assertIsNotNone(duration)

    def test_execute_commands_straight_line_vertical_case(self):
        commands = [
            {"direction": "south", "steps": 2},
            {"direction": "north", "steps": 2},
        ]
        x, y = 0, 0
        result, duration = execute_commands(commands, x, y)
        self.assertEqual(result, 3)
        self.assertIsNotNone(duration)

    def test_execute_commands_loop_2x2(self):
        commands = [
            {"direction": "east", "steps": 2},
            {"direction": "south", "steps": 2},
            {"direction": "west", "steps": 2},
            {"direction": "north", "steps": 2},
            {"direction": "east", "steps": 2},
            {"direction": "south", "steps": 2},
            {"direction": "west", "steps": 2},
            {"direction": "north", "steps": 2},
        ]
        x, y = 0, 0
        result, duration = execute_commands(commands, x, y)
        self.assertEqual(result, 8)
        self.assertIsNotNone(duration)

    def test_execute_commands_loop_100x100(self):
        commands = [
            {"direction": "east", "steps": 100},
            {"direction": "south", "steps": 100},
            {"direction": "west", "steps": 100},
            {"direction": "north", "steps": 100},
            {"direction": "east", "steps": 100},
            {"direction": "south", "steps": 100},
            {"direction": "west", "steps": 100},
            {"direction": "north", "steps": 100},
        ]
        x, y = 0, 0
        result, duration = execute_commands(commands, x, y)
        self.assertEqual(result, 400)
        self.assertIsNotNone(duration)


if __name__ == "__main__":
    unittest.main()
