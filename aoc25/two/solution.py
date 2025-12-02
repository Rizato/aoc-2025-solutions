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
            if not ProductRange.is_id_valid_part_two(i)
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

    @staticmethod
    def is_id_valid_part_two(product_id: int) -> bool:
        # Now test if the number has some number of repeating patterns
        # Two pointer solution in one pass
        repeat_pointer = 0
        current_pointer = 1
        # We could do this without converting to a string...

        pid = product_id
        p = list()
        while pid > 0:
            p.insert(0, pid % 10)
            pid //= 10

        while current_pointer < len(p):
            # Rest when they don't match
            # This handles things like 11121112, so it will reset back to the start, even when matching numbers within a pattern
            if p[current_pointer] == p[repeat_pointer]:
                repeat_pointer += 1
            elif p[current_pointer] == p[0]:
                # If it matches the starting position, start over but with a match already
                repeat_pointer = 1
            else:
                repeat_pointer = 0

            current_pointer += 1

        # Now, we have a repeat pointer and current pointer
        # repeater pointer is a multiple of the difference, then it matched
        # Also have to check 0 to make sure it found any match at all
        diff = current_pointer - repeat_pointer
        return repeat_pointer == 0 or repeat_pointer % diff != 0

    @classmethod
    def parse_range(cls, products: str) -> Self:
        parts = products.split("-")
        if len(parts) != 2:
            raise ValueError(f"Invalid range: {products}")

        return cls(int(parts[0]), int(parts[1]))


def run() -> int:
    with open("input.txt", "r") as f:
        return sum(
            [
                invalid
                for p in f.read().split(",")
                for invalid in ProductRange.parse_range(p).find_invalid_ids()
            ]
        )


if __name__ == "__main__":
    print(run())
