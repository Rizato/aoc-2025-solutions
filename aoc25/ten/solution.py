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


@dataclasses.dataclass
class Machine:
    lights: IndicatorLights
    buttons: List[Button]

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


class DiagramParser:

    @staticmethod
    def parse(junctions: str) -> List[Machine]:
        machines = []
        for line in junctions.splitlines():
            if not line.strip():
                continue

            # find indicators, which are surrounded by brackets
            close_bracket_index = line.index("]")
            light_goals = line[1:close_bracket_index]
            lights = IndicatorLights(
                [i for i, c in enumerate(light_goals) if c == "#"], len(light_goals)
            )

            # find buttons - can by many
            buttons = []
            index = close_bracket_index + 1
            buttons_groups = line[index:].split(" ")
            for button_str in buttons_groups:
                if not button_str.strip() or ")" not in button_str:
                    continue
                end_index = button_str.index(")")
                button = Button([int(b) for b in button_str[1:end_index].split(",")])
                buttons.append(button)
            # ignore joltage for part 1
            machines.append(Machine(lights, buttons))
        return machines


def run() -> int:

    with open("input.txt", "r") as f:
        machines = DiagramParser().parse(f.read())

    return sum(machine.find_min_button_presses() for machine in machines)


if __name__ == "__main__":
    print(run())
