import unittest
from app.execute_commands import execute_commands_v2, execute_commands_v1
import matplotlib.pyplot as plt


class TestAlgorithmPerformance(unittest.TestCase):
    def test_time_complexity_square(self):
        plt.figure()
        plt.title("Algorithm Performance - square Path")
        plt.xlabel("Commands + Steps")
        plt.ylabel("Execution Duration (s)")
        plt.grid()

        x_values_v2, y_values_v2 = [], []
        x_values_v1, y_values_v1 = [], []

        for size in range(100):
            # testing multiple loops
            commands = []
            for _ in range(size):
                commands.extend(
                    [
                        {"direction": "east", "steps": size},
                        {"direction": "south", "steps": size},
                        {"direction": "west", "steps": size},
                        {"direction": "north", "steps": size},
                    ]
                )

            _, execution_time_new = execute_commands_v2(commands, 0, 0)
            _, execution_time_old = execute_commands_v1(commands, 0, 0)
            total_commands = len(commands)
            total_steps = sum(cmd["steps"] for cmd in commands)
            x_values_v2.append(total_commands + total_steps)
            y_values_v2.append(execution_time_new)
            x_values_v1.append(total_commands + total_steps)
            y_values_v1.append(execution_time_old)

        plt.plot(
            x_values_v2,
            y_values_v2,
            marker="o",
            linestyle="-",
            label="Algorithm V1",
        )
        plt.plot(
            x_values_v1,
            y_values_v1,
            marker="x",
            linestyle="--",
            label="Algorithm V2",
        )
        plt.legend()
        plt.savefig(
            "./app/tests/performance_tests/duration_vs_commands_steps_square.png"
        )
        print("Graph saved as 'duration_vs_commands_steps_square.png'")

    def test_time_complexity_al_dente(self):
        plt.figure()
        plt.title("Algorithm Performance - Dente Path")
        plt.xlabel("Commands + Steps")
        plt.ylabel("Execution Duration (s)")
        plt.grid()

        x_values_v2, y_values_v2 = [], []
        x_values_v1, y_values_v1 = [], []

        for size in range(500):
            commands = []
            for _ in range(size):
                commands.extend(
                    [
                        {"direction": "east", "steps": 1},
                        {"direction": "south", "steps": 1},
                        {"direction": "east", "steps": 1},
                        {"direction": "north", "steps": 1},
                    ]
                )

            _, execution_time_new = execute_commands_v2(commands, 0, 0)
            _, execution_time_old = execute_commands_v1(commands, 0, 0)
            total_commands = len(commands)
            total_steps = sum(cmd["steps"] for cmd in commands)
            x_values_v2.append(total_commands + total_steps)
            y_values_v2.append(execution_time_new)
            x_values_v1.append(total_commands + total_steps)
            y_values_v1.append(execution_time_old)

        plt.plot(
            x_values_v2,
            y_values_v2,
            marker="o",
            linestyle="-",
            label="Algorithm V1",
        )
        plt.plot(
            x_values_v1,
            y_values_v1,
            marker="x",
            linestyle="--",
            label="Algorithm V2",
        )
        plt.legend()
        plt.savefig(
            "./app/tests/performance_tests/duration_vs_commands_steps_dente.png"
        )
        print("Graph saved as 'duration_vs_commands_steps_dente.png'")


if __name__ == "__main__":
    unittest.main()
