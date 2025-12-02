import dataclasses
from typing import List, Self


@dataclasses.dataclass(frozen=True)
class ProductRange:
    start: int
    end: int

    def find_invalid_ids(self) -> List[int]:
        return [
            i
            for i in range(self.start, self.end + 1)
            if not ProductRange.is_id_valid(i)
        ]

    @staticmethod
    def is_id_valid(product_id: int) -> bool:
        # The test is if it repeats itself, not if it repeats any digit
        pid = str(product_id)
        size = len(pid)
        # Cannot be a repeating pattern if uneven. We should prune this earlier
        if size % 2 != 0:
            return True

        first_half = pid[: size // 2]
        second_half = pid[size // 2 :]
        return first_half != second_half

    @classmethod
    def parse_range(cls, products: str) -> Self:
        parts = products.split("-")
        if len(parts) != 2:
            raise ValueError(f"Invalid range: {products}")

        return cls(int(parts[0]), int(parts[1]))


def run() -> int:
    with open("input.txt", "r") as f:
        product_ranges = [ProductRange.parse_range(p) for p in f.read().split(",")]

    return sum([invalid for p in product_ranges for invalid in p.find_invalid_ids()])


if __name__ == "__main__":
    print(run())
