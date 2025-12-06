import dataclasses
import enum
from typing import List, Tuple


class CounterState(enum.Enum):
    RANGES = enum.auto()
    IDS = enum.auto()


@dataclasses.dataclass
class FreshRange:
    lower: int
    upper: int

    def __len__(self):
        if self.upper < self.lower:
            return 0

        return self.upper - self.lower + 1

    def __contains__(self, other: int) -> bool:
        return self.lower <= other <= self.upper


class Inventory:

    def __init__(self, fresh_ranges: List[FreshRange]) -> None:
        self.fresh_ranges = fresh_ranges

    def get_num_fresh(self, query: List[int]) -> int:
        c = 0
        for query_id in query:
            for fresh_range in self.fresh_ranges:
                if query_id in fresh_range:
                    c += 1
                    break

        return c

    def get_num_total_inventory(self) -> int:
        total = 0
        for i, fresh_range in enumerate(self.fresh_ranges):
            for j in range(len(self.fresh_ranges)):
                if i == j:
                    continue

                # skip the rest in this case
                if fresh_range.upper < fresh_range.lower:
                    continue

                check_range = self.fresh_ranges[j]
                if fresh_range.lower in check_range:
                    fresh_range.lower = check_range.upper + 1

                if fresh_range.upper in check_range:
                    fresh_range.upper = check_range.lower - 1

            total += len(fresh_range)

        return total

    def get_num_total_inventory_slow(self) -> int:
        ids = set()
        for fresh_range in self.fresh_ranges:
            for i in range(fresh_range.lower, fresh_range.upper + 1):
                ids.add(i)

        return len(ids)


class DatabaseParser:

    def parse(self, database: str) -> Tuple[Inventory, List[int]]:
        fresh_ranges = []
        query_ids = []
        state = CounterState.RANGES
        for line in database.split("\n"):
            if state == CounterState.RANGES and not line.strip():
                state = CounterState.IDS
                continue

            if state == CounterState.RANGES:
                low = int(line.split("-")[0])
                high = int(line.split("-")[1])
                fresh_ranges.append(FreshRange(low, high))
            else:
                query_ids.append(int(line))

        return Inventory(fresh_ranges), query_ids


def run() -> int:

    with open("input.txt", "r") as f:
        inventory, query_ids = DatabaseParser().parse(f.read())

    return inventory.get_num_total_inventory()


if __name__ == "__main__":
    print(run())
