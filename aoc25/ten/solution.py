import dataclasses
import heapq
from collections import deque
from typing import List, Optional, Set, Tuple, Deque, Dict


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
        # this is more complicated as we can press each button multiple times
        goal = self.joltage.goal
        initial: Tuple[int, ...] = tuple([0] * len(self.joltage.joltages))

        # track a heap with estimated, current, and state
        heap: List[Tuple[int, int, Tuple[int, ...]]] = [
            (self.heuristic(initial), 0, initial)
        ]
        cache: Dict[Tuple[int, ...], int] = dict()
        # Track a list to the current state
        cache[tuple(initial)] = 0
        while heap:
            estimated, score, current = heapq.heappop(heap)

            # if our score was lowered by some other pass, we can skip
            if current in cache and cache[current] < score:
                continue

            for button in self.buttons:
                updated_score = score + 1
                # increment each i if that index is in the button
                updated_joltage = tuple(
                    v + 1 if i in button.values else v for i, v in enumerate(current)
                )

                if all(j == g for j, g in zip(updated_joltage, goal)):
                    return updated_score

                if any(
                    updated_joltage[i] > self.joltage.goal[i]
                    for i in range(len(updated_joltage))
                ):
                    continue

                if (
                    not updated_joltage in cache
                    or cache[updated_joltage] > updated_score
                ):
                    cache[updated_joltage] = updated_score
                    updated_estimate = updated_score + self.heuristic(updated_joltage)

                    heapq.heappush(
                        heap, (updated_estimate, updated_score, updated_joltage)
                    )

        if tuple(goal) in cache:
            return cache[tuple(goal)]
        raise ValueError

    def heuristic(self, current: Tuple[int, ...]) -> int:
        # find the min difference between any button and the goal at the same index
        return sum([g - c for c, g in zip(current, self.joltage.goal)])


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
