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
        if not self.fresh_ranges:
            return 0

        merged_fresh = []
        current = None
        for fresh in sorted(self.fresh_ranges, key=lambda x: x.lower):
            if not current:
                current = fresh
                continue

            if current.upper < fresh.lower:
                # We do not overlap, so add current, and move on
                merged_fresh.append(current)
                current = fresh
            else:
                # we do overlap, so merge them, knowing that we started with current.lower the lower (or equal) by sorting
                current = FreshRange(current.lower, max(current.upper, fresh.upper))

        # merge the last one at the end of the loop
        merged_fresh.append(current)

        return sum(len(fresh) for fresh in merged_fresh)

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
