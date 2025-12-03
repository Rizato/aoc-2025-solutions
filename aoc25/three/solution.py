import dataclasses
from typing import List, Self


@dataclasses.dataclass(frozen=True)
class BatteryBank:
    batteries: List[int]

    @classmethod
    def parse_bank(cls, value: str) -> Self:
        return cls([int(a) for a in value])


class JoltageCalculator:
    def __init__(self):
        self.total_joltage = 0

    def add_max_joltage(self, bank: BatteryBank):
        self.total_joltage += self.find_max_joltage(bank)

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


def run() -> int:
    calc = JoltageCalculator()
    with open("input.txt", "r") as f:
        for line in f.readlines():
            if not line.strip():
                continue

            bank = BatteryBank.parse_bank(line.strip())
            calc.add_max_joltage(bank)

    return calc.total_joltage


if __name__ == "__main__":
    print(run())
