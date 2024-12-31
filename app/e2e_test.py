import unittest
import requests
import time
import matplotlib.pyplot as plt

BASE_URL = "http://localhost:5000/tibber-developer-test/enter-path"


class TestEnterPathE2E(unittest.TestCase):

    def test_basic_execution(self):
        payload = {
            "start": {"x": 10, "y": 22},
            "commmands": [
                {"direction": "east", "steps": 2},
                {"direction": "north", "steps": 1},
            ],
        }  # example case given in the assignment
        response = requests.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["result"], 4)
        self.assertGreater(data["duration"], 0)

    def test_large_execution(self):
        commands = [{"direction": "north", "steps": 1} for _ in range(1000)]
        payload = {"start": {"x": 0, "y": 0}, "commmands": commands}
        response = requests.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["result"], 1001)
        self.assertGreater(data["duration"], 0)

    def test_time_complexity(self):
        plt.figure()
        plt.title("Relationship Between Duration and Commands+Steps")
        plt.xlabel("Commands + Steps")
        plt.ylabel("Execution Duration (s)")
        plt.legend()
        plt.grid()

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

            payload = {"start": {"x": 0, "y": 0}, "commmands": commands}

            start_time = time.time()
            response = requests.post(BASE_URL, json=payload)
            end_time = time.time()

            self.assertEqual(response.status_code, 201)
            data = response.json()

            # Check relationship between number of commands and execution time
            execution_time = end_time - start_time
            self.assertLess(
                data["duration"], execution_time
            )  # Ensure server-side timing is accurate

            plot_execution_time(commands, data["duration"])

        plt.savefig("duration_vs_commands_steps.png")
        print("Graph saved as 'duration_vs_commands_steps.png'")


def plot_execution_time(commands, duration):
    total_commands = len(commands)
    total_steps = sum(cmd["steps"] for cmd in commands)

    # Plotting graph of duration vs (commands + steps)
    x_values = [total_commands + total_steps]
    y_values = [duration]

    plt.plot(
        x_values,
        y_values,
        marker="o",
        linestyle="-",
        label="Duration vs Commands+Steps",
    )


if __name__ == "__main__":
    unittest.main()
