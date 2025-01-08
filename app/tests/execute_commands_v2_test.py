import unittest
from app.execute_commands_v2 import (
    Line,
    calculate_crossings,
    count_points,
    create_lines,
    execute_commands_v2,
    merge_segments,
)


class TestExecuteCommands(unittest.TestCase):
    # create_lines
    def test_create_lines(self):
        commands = [
            {"direction": "north", "steps": 2},
            {"direction": "east", "steps": 2},
            {"direction": "south", "steps": 2},
            {"direction": "west", "steps": 2},
            {"direction": "north", "steps": 2},
            {"direction": "east", "steps": 2},
            {"direction": "south", "steps": 2},
            {"direction": "west", "steps": 2},
        ]

        horizontal_lines, vertical_lines = create_lines(0, 0, commands)

        self.assertEqual(len(horizontal_lines), 4)
        self.assertEqual(horizontal_lines[0], Line(2, 0, 2))
        self.assertEqual(horizontal_lines[1], Line(0, 0, 2))
        self.assertEqual(horizontal_lines[2], Line(2, 0, 2))
        self.assertEqual(horizontal_lines[3], Line(0, 0, 2))

        self.assertEqual(len(vertical_lines), 4)
        self.assertEqual(vertical_lines[0], Line(0, 0, 2))
        self.assertEqual(vertical_lines[1], Line(2, 0, 2))
        self.assertEqual(vertical_lines[2], Line(0, 0, 2))

    # merge_segments
    def test_merge_segments_same_direction(self):
        merged = merge_segments(
            [
                Line(0, 0, 2),
                Line(0, 0, 2),
            ]
        )
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0].constant, 0)
        self.assertEqual(merged[0].start, 0)
        self.assertEqual(merged[0].end, 2)

        merged = merge_segments(
            [
                Line(0, 0, 2),
                Line(0, 2, 4),
            ]
        )
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0].constant, 0)
        self.assertEqual(merged[0].start, 0)
        self.assertEqual(merged[0].end, 4)

    def test_count_points(self):
        self.assertEqual(
            count_points(
                [
                    Line(0, 0, 2),
                    Line(0, 2, 4),
                ]
            ),
            6,
        )

    # count_crossings
    def test_count_crossings(self):
        vertical_lines = [Line(0, 0, 4), Line(2, 2, 4)]
        horizontal_lines = [Line(2, -2, 2), Line(4, 0, 2)]
        self.assertEqual(calculate_crossings(vertical_lines, horizontal_lines), 4)

    # execute_commands_v2
    def test_execute_commands_no_steps(self):
        commands = [
            {"direction": "north", "steps": 0},
        ]
        x, y = 0, 0
        result, duration = execute_commands_v2(commands, x, y)
        self.assertEqual(result, 1)  # Only the start position
        self.assertIsNotNone(duration)

    def test_execute_commands_successful_output(self):
        commands = [
            {"direction": "north", "steps": 1},
            {"direction": "east", "steps": 1},
            {"direction": "south", "steps": 1},
            {"direction": "west", "steps": 1},
        ]
        x, y = 0, 0
        result, duration = execute_commands_v2(commands, x, y)
        self.assertEqual(result, 4)
        self.assertIsNotNone(duration)

    def test_execute_commands_straight_line_horizontal_case(self):
        commands = [
            {"direction": "east", "steps": 2},
            {"direction": "west", "steps": 2},
        ]
        x, y = 0, 0
        result, duration = execute_commands_v2(commands, x, y)
        self.assertEqual(result, 3)
        self.assertIsNotNone(duration)

    def test_execute_commands_straight_line_vertical_case(self):
        commands = [
            {"direction": "south", "steps": 2},
            {"direction": "north", "steps": 2},
        ]
        x, y = 0, 0
        result, duration = execute_commands_v2(commands, x, y)
        self.assertEqual(result, 3)
        self.assertIsNotNone(duration)

    def test_execute_commands_large_input(self):
        commands = [{"direction": "north", "steps": 1} for _ in range(10000)]
        x, y = 0, 0
        result, duration = execute_commands_v2(commands, x, y)
        self.assertEqual(result, 10001)
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
        result, duration = execute_commands_v2(commands, x, y)
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
        result, duration = execute_commands_v2(commands, x, y)
        self.assertEqual(result, 400)
        self.assertIsNotNone(duration)

    def test_execute_commands_teeth(self):
        commands = [
            {"direction": "east", "steps": 2},
            {"direction": "north", "steps": 4},
            {"direction": "east", "steps": 2},
            {"direction": "south", "steps": 4},
            {"direction": "east", "steps": 2},
            {"direction": "north", "steps": 2},
            {"direction": "west", "steps": 8},
        ]
        x, y = 0, 0
        result, duration = execute_commands_v2(commands, x, y)
        self.assertEqual(result, 23)
        self.assertIsNotNone(duration)


if __name__ == "__main__":
    unittest.main()
