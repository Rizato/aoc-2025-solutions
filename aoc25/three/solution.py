import dataclasses
from typing import List, Self


@dataclasses.dataclass(frozen=True)
class BatteryBank:
    batteries: List[int]

    @classmethod
    def parse_bank(cls, value: str) -> Self:
        return cls([int(a) for a in value])


class JoltageCalculator:
    def __init__(self, active_cells: int):
        self.active_cells = active_cells
        self.total_joltage = 0

    def add_max_joltage(self, bank: BatteryBank):
        self.total_joltage += self.find_max_joltage_part_two_dp(bank, self.active_cells)

    @staticmethod
    def find_max_joltage(bank: BatteryBank) -> int:
        # This is a greedy algorithm because forced ltr
        tens_digit = 0
        ones_digit = 0
        for i in range(len(bank.batteries)):
            # Basically step up the 10s and ones digits as I go through if they are higher
            # Set the 10s digit if greater, and not the last number
            if bank.batteries[i] > tens_digit and i + 1 < len(bank.batteries):
                tens_digit = bank.batteries[i]
                ones_digit = bank.batteries[i + 1]
            elif bank.batteries[i] > ones_digit:
                # set the ones digit if greater
                ones_digit = bank.batteries[i]

        return tens_digit * 10 + ones_digit

    @staticmethod
    def find_max_joltage_part_two_dp(bank: BatteryBank, to_activate: int) -> int:
        # activate only the active cells
        # I believe this is a dynamic programming problem...
        # At each stage we can cache the largest number to that point...
        # we can work backwards to build the largest number
        # dp = []
        # for battery in reversed(bank.batteries):
        # we want the maximum at every point while working forward
        # if we have less than 12 length....

        # if we have 12 length, replace 12th digit with self
        # but that will just end up wrong, because we need to replace the right number
        # so create the maximally large number with the smallest number of digits?

        # alternatively, we could find the largest numbers between the start and final 11 numbers
        # then, our search range is from last found + 1 to final 10 numbers (total - 1 - found)
        # this will basically be O(n * 12)
        # But to_activate is now a property, so O(n * m)
        # not the fastest, but should work
        front = 0
        digits = [0] * to_activate
        # find to_activate digits
        for i in range(to_activate):
            # start from previous found, until the
            max_digit = 0

            # Ensure that you always pick a number before the last 12
            for j in range(front, len(bank.batteries) - to_activate + i + 1):
                if bank.batteries[j] > max_digit:
                    max_digit = bank.batteries[j]
                    digits[i] = max_digit
                    # Reduce the scope of the search from the next onward
                    front = j + 1

        return sum(i * 10**power for power, i in enumerate(reversed(digits)))


def run() -> int:
    calc = JoltageCalculator(12)
    with open("input.txt", "r") as f:
        for line in f.readlines():
            if not line.strip():
                continue

            bank = BatteryBank.parse_bank(line.strip())
            calc.add_max_joltage(bank)

    return calc.total_joltage


if __name__ == "__main__":
    print(run())
