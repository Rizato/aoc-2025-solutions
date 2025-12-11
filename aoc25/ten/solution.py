import dataclasses
from typing import List, Optional


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
        self.joltages[index] = not self.joltages[index]

    def test(self) -> bool:
        return self.goal == self.joltages


@dataclasses.dataclass
class Machine:
    lights: IndicatorLights
    buttons: List[Button]
    joltage: JoltagePanel

    def find_min_button_presses(self):
        valid_heights = []
        height = 0

        def press_button(index: int):
            # try pressing, then not pressing, then go to the next button in each case
            if index >= len(self.buttons):
                return

            nonlocal height
            # Press sequence
            height += 1
            self.press_button(self.buttons[index])
            matches = self.lights.test()
            if matches:
                valid_heights.append(height)
            else:
                # move onto the next button if we don't match
                press_button(index + 1)

            # Reset from press sequence
            height -= 1
            self.press_button(self.buttons[index])
            # no need to check further with off, the best we could do is tie this result
            if matches:
                return

            # Try next buttons again, with us off this time
            press_button(index + 1)

        press_button(0)

        if valid_heights:
            return min(valid_heights)

        raise ValueError

    def press_button(self, button: Button):
        for m in button.values:
            self.lights.flip(m)

    def find_min_button_presses_joltage(self):
        # this is more complicated as we can press each button multiple times
        valid_heights = []
        height = 0

        def press_button(index: int):
            # try pressing, then not pressing, then go to the next button in each case
            if index >= len(self.buttons):
                return

            nonlocal height
            # Press sequence
            height += 1
            self.press_button(self.buttons[index])
            matches = self.lights.test()
            if matches:
                valid_heights.append(height)
            else:
                # move onto the next button if we don't match
                press_button(index + 1)

            # Reset from press sequence
            height -= 1
            self.press_button(self.buttons[index])
            # no need to check further with off, the best we could do is tie this result
            if matches:
                return

            # Try next buttons again, with us off this time
            press_button(index + 1)

        press_button(0)

        if valid_heights:
            return min(valid_heights)

        raise ValueError

    def press_button_joltage(self, button: Button):
        for m in button.values:
            self.joltage.increment(m)


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

            joltage = JoltagePanel([int(joltage) for joltage in "".join(rest)[:-1].split(",")])
            machines.append(Machine(lights, buttons, joltage))
        return machines


def run() -> int:

    with open("input.txt", "r") as f:
        machines = DiagramParser().parse(f.read())

    return sum(machine.find_min_button_presses_joltage() for machine in machines)


if __name__ == "__main__":
    print(run())
