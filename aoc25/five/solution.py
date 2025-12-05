import dataclasses
import enum
from collections import deque
from typing import Self


class CounterState(enum.Enum):
    RANGES = enum.auto()
    IDS = enum.auto()

@dataclasses.dataclass(frozen=True)
class FreshRange:
    lower: int
    upper: int

    def __contains__(self, other: int) -> bool:
        return self.lower <= other <= self.upper


class FreshCounter:

    def __init__(self):
        self.fresh_ranges = list()
        self.state = CounterState.RANGES

    def count_fresh(self, inventory: str) -> int:
        c = 0
        for line in inventory.split("\n"):
            if self.state == CounterState.RANGES and not line.strip():
                self.state = CounterState.IDS
                continue

            if self.state == CounterState.RANGES:
                low = int(line.split("-")[0])
                high = int(line.split("-")[1])
                self.fresh_ranges.append(FreshRange(low, high))
            else:
                check = int(line)
                for fresh_range in self.fresh_ranges:
                    if check in fresh_range:
                        c += 1
                        break

        return c

def run() -> int:

    fresh_counter = FreshCounter()
    with open("input.txt", "r") as f:
        fresh = fresh_counter.count_fresh(f.read())

    return fresh


if __name__ == "__main__":
    print(run())
