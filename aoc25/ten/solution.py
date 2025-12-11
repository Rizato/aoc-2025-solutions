import dataclasses
from collections import deque
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
        # this first solution creates a tree of every possible option
        # then iterates across it to find all the valid solutions
        # then it grabs the minimum solution
        root = TreeNode(None)
        previous_row = [root]
        next_row = []
        for button in self.buttons:
            for node in previous_row:
                node.on = TreeNode(button)
                node.off = TreeNode(button)
                next_row.extend([node.off, node.on])
            previous_row = next_row
            next_row = []

        stack = deque()
        valid_heights = []

        # this is looking for the minimum, with a series of sub-problems... is this dp?
        def press_button(tree_node: TreeNode, press: bool):
            if not tree_node:
                return

            # press button
            # if not right, call on then off
            if press:
                stack.appendleft(tree_node)
                self.press_button(tree_node.value)

                # mark if correct
                if self.lights.test():
                    valid_heights.append(len(stack))
                    # reset the button
                    if press:
                        stack.popleft()
                        self.press_button(tree_node.value)
                    return

            # run over the children
            if tree_node.on:
                press_button(tree_node.on, True)
            if tree_node.off:
                press_button(tree_node.off, False)
            # reset the button
            if press:
                stack.popleft()
                self.press_button(tree_node.value)

        press_button(root.on, True)
        stack.clear()
        press_button(root.off, False)

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
