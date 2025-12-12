import dataclasses
from typing import List, Optional

from z3 import Int, Optimize, Sum, sat


@dataclasses.dataclass
class Button:
    values: List[int]


@dataclasses.dataclass
class TreeNode:
    value: Optional[Button] = None
    on: Optional["TreeNode"] = None
    off: Optional["TreeNode"] = None


class IndicatorLights:
    lights: List[bool]
    goal: List[int]

    def __init__(self, goal: List[int], size: int):
        self.goal = goal
        # initialize lights all off
        self.lights = [False] * size

    def flip(self, index: int):
        self.lights[index] = not self.lights[index]

    def test(self) -> bool:
        on_lights = [i for i, l in enumerate(self.lights) if l]
        return self.goal == on_lights


class JoltagePanel:
    joltages: List[int]
    goal: List[int]

    def __init__(self, goal: List[int]):
        self.goal = goal
        # initialize joltages to 0
        self.joltages = [0] * len(goal)

    def increment(self, index: int):
        self.joltages[index] += 1

    def is_too_high(self):
        for i, joltage in enumerate(self.joltages):
            if joltage > self.goal[i]:
                return True

        return False

    def test(self) -> bool:
        return self.goal == self.joltages

    def reset(self):
        self.joltages = [0] * len(self.joltages)


@dataclasses.dataclass
class Machine:
    lights: IndicatorLights
    buttons: List[Button]
    joltage: JoltagePanel

    def find_min_button_presses(self):
        valid_heights = []

        def press_button(index: int, height: int):
            # try pressing, then not pressing, then go to the next button in each case
            if index >= len(self.buttons):
                return

            # Press sequence
            self.press_button(self.buttons[index])
            matches = self.lights.test()
            if matches:
                valid_heights.append(height + 1)
            else:
                # move onto the next button if we don't match
                press_button(index + 1, height + 1)

            # Reset from press sequence
            self.press_button(self.buttons[index])
            # no need to check further with off, the best we could do is tie this result
            if matches:
                return

            # Try next buttons again, with us off this time
            press_button(index + 1, height)

        press_button(0, 0)

        if valid_heights:
            return min(valid_heights)

        raise ValueError

    def press_button(self, button: Button):
        for m in button.values:
            self.lights.flip(m)

    def find_min_button_presses_joltage(self) -> int:
        """
        Solve using Z3 SMT solver for integer linear programming.

        Problem: minimize Σxᵢ subject to Ax = b, x ≥ 0, x ∈ ℤⁿ
        Where:
        - A[i,j] = 1 if button j affects position i, else 0
        - b = goal vector
        - x = vector of button press counts
        """
        goal = self.joltage.goal
        num_positions = len(goal)
        num_buttons = len(self.buttons)
        return self._solve_with_z3(goal, num_positions, num_buttons)

    def _solve_with_z3(
        self, goal: List[int], num_positions: int, num_buttons: int
    ) -> int:
        """Solve using Z3 SMT solver."""
        # Create integer variables for button press counts
        x = [Int(f"x_{i}") for i in range(num_buttons)]

        # Create optimizer
        opt = Optimize()

        # Constraints: x[i] >= 0 for all buttons
        for i in range(num_buttons):
            opt.add(x[i] >= 0)

        # Constraints: For each position, sum of button presses affecting it equals goal
        for pos in range(num_positions):
            # Sum of all buttons that affect this position
            affecting_buttons = [
                x[btn_idx]
                for btn_idx, button in enumerate(self.buttons)
                if pos in button.values
            ]
            if affecting_buttons:
                opt.add(Sum(affecting_buttons) == goal[pos])
            else:
                # No button affects this position, so goal must be 0
                if goal[pos] != 0:
                    raise ValueError(
                        f"Position {pos} requires {goal[pos]} but no button affects it"
                    )

        # Objective: minimize sum of all button presses
        opt.minimize(Sum(x))

        # Solve
        if opt.check() == sat:
            model = opt.model()
            total = sum(model[x[i]].as_long() for i in range(num_buttons))
            return total
        else:
            raise ValueError("No solution found")


class DiagramParser:

    @staticmethod
    def parse(junctions: str) -> List[Machine]:
        machines = []
        for line in junctions.splitlines():
            if not line.strip():
                continue

            # find indicators, which are surrounded by brackets
            light, *rest = line.split("]")
            lights = IndicatorLights(
                [i for i, c in enumerate(light[1:]) if c == "#"], len(light) - 1
            )

            button_split, *rest = "".join(rest).split("{")
            # find buttons - can be many
            buttons = []
            buttons_groups = button_split.split(" ")
            for button_str in buttons_groups:
                if not button_str.strip() or ")" not in button_str:
                    continue
                end_index = button_str.index(")")
                button = Button([int(b) for b in button_str[1:end_index].split(",")])
                buttons.append(button)

            joltage = JoltagePanel(
                [int(joltage) for joltage in "".join(rest)[:-1].split(",")]
            )
            machines.append(Machine(lights, buttons, joltage))
        return machines


def run() -> int:

    with open("input.txt", "r") as f:
        machines = DiagramParser().parse(f.read())

    return sum(machine.find_min_button_presses_joltage() for machine in machines)


if __name__ == "__main__":
    print(run())
