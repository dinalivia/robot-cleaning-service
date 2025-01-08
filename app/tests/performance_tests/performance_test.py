import unittest
from app.execute_commands_v1 import execute_commands_v1
from app.execute_commands_v2 import execute_commands_v2
import matplotlib.pyplot as plt


class TestAlgorithmPerformance(unittest.TestCase):
    def test_time_complexity_square(self):
        plt.figure()
        plt.title("Algorithm Performance - square Path")
        plt.xlabel("Steps")
        plt.ylabel("Execution Duration (s)")
        plt.grid()

        x_values_new, y_values_new = [], []
        x_values_old, y_values_old = [], []

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

            _, execution_time_old = execute_commands_v1(commands, 0, 0)
            _, execution_time_new = execute_commands_v2(commands, 0, 0)

            total_commands = len(commands)
            total_steps = sum(cmd["steps"] for cmd in commands)
            x_values_new.append(total_steps)
            y_values_new.append(execution_time_new)
            x_values_old.append(total_steps)
            y_values_old.append(execution_time_old)

        plt.plot(
            x_values_old,
            y_values_old,
            marker="x",
            linestyle="--",
            label="Algorithm V1",
        )
        plt.plot(
            x_values_new,
            y_values_new,
            marker="o",
            linestyle="-",
            label="Algorithm V2",
        )
        plt.legend()
        plt.savefig("./images/duration_vs_commands_steps_square.png")
        print("Graph saved as 'duration_vs_commands_steps_square.png'")

    def test_time_complexity_al_dente(self):
        plt.figure()
        plt.title("Algorithm Performance - teeth Path")
        plt.xlabel("Steps")
        plt.ylabel("Execution Duration (s)")
        plt.grid()

        x_values_new, y_values_new = [], []
        x_values_old, y_values_old = [], []

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

            _, execution_time_old = execute_commands_v1(commands, 0, 0)
            _, execution_time_new = execute_commands_v2(commands, 0, 0)

            total_commands = len(commands)
            total_steps = sum(cmd["steps"] for cmd in commands)
            x_values_new.append(total_steps)
            y_values_new.append(execution_time_new)
            x_values_old.append(total_steps)
            y_values_old.append(execution_time_old)

        plt.plot(
            x_values_old,
            y_values_old,
            marker="x",
            linestyle="--",
            label="Algorithm V1",
        )
        plt.plot(
            x_values_new,
            y_values_new,
            marker="o",
            linestyle="-",
            label="Algorithm V2",
        )
        plt.legend()
        plt.savefig("./images/duration_vs_steps_teeth_path.png")
        print("Graph saved as 'duration_vs_steps_teeth_path.png'")

    def test_time_complexity_realistic_path(self):
        plt.figure()
        plt.title("Algorithm Performance - realistic Path")
        plt.xlabel("Steps")
        plt.ylabel("Execution Duration (s)")
        plt.grid()

        x_values_new, y_values_new = [], []
        x_values_old, y_values_old = [], []

        commands = []
        last_time_v1 = 0
        last_time_v2 = 0
        while len(commands) <= 10000:
            print("number of commands", len(commands))
            print("last_time_v1", last_time_v1)
            print("last_time_v2", last_time_v2)

            # for _ in range(size):
            commands.extend(
                [
                    {"direction": "north", "steps": 100000},
                    {"direction": "east", "steps": 1},
                    {"direction": "south", "steps": 100000},
                    {"direction": "east", "steps": 1},
                ]
            )

            total_steps = sum(cmd["steps"] for cmd in commands)

            if last_time_v1 <= 1:
                _, execution_time_old = execute_commands_v1(commands, 0, 0)
                last_time_v1 = execution_time_old
                x_values_old.append(total_steps)
                y_values_old.append(execution_time_old)

            if last_time_v2 <= 1:
                _, execution_time_new = execute_commands_v2(commands, 0, 0)
                last_time_v2 = execution_time_new
                x_values_new.append(total_steps)
                y_values_new.append(execution_time_new)

            if last_time_v1 > 1 and last_time_v2 > 1:
                break

        plt.plot(
            x_values_old,
            y_values_old,
            marker="x",
            linestyle="--",
            label="Algorithm V1",
        )
        plt.plot(
            x_values_new,
            y_values_new,
            marker="o",
            linestyle="-",
            label="Algorithm V2",
        )
        plt.legend()
        plt.savefig("./images/duration_vs_commands_steps_realistic.png")
        print("Graph saved as 'duration_vs_commands_steps_realistic.png'")


if __name__ == "__main__":
    unittest.main()
