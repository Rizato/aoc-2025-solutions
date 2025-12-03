import dataclasses
from typing import Iterable, List, Optional, Self


def list_to_int(digits: Iterable) -> int:
    total = 0
    for i in digits:
        total *= 10
        total += int(i)

    return total


class LinkedListIterator:
    def __init__(self, head: Optional["ListNode"] = None):
        self.head = head

    def __next__(self):
        if self.head is None:
            raise StopIteration

        value = self.head.value
        self.head = self.head.next
        return value


class ListNode:
    value: int
    next: Optional["ListNode"] = None
    prev: Optional["ListNode"] = None

    def __init__(self, value):
        self.value = value

    def __iter__(self):
        return LinkedListIterator(self)

    def __repr__(self):
        return f"ListNode({self.value})"


@dataclasses.dataclass(frozen=True)
class BatteryBank:
    cells: List[int]

    @classmethod
    def parse_bank(cls, value: str) -> Self:
        return cls([int(a) for a in value])


class JoltageCalculator:
    def __init__(self, num_active_cells: int):
        self.num_active_cells = num_active_cells
        self.total_joltage = 0

    def add_max_joltage(self, bank: BatteryBank):
        self.total_joltage += self.find_max_joltage_part_two_linear(
            bank, self.num_active_cells
        )

    @staticmethod
    def find_max_joltage_part_one(bank: BatteryBank) -> int:
        # This is a greedy algorithm because forced ltr
        tens_digit = 0
        ones_digit = 0
        for i in range(len(bank.cells)):
            # Basically step up the 10s and ones digits as I go through if they are higher
            # Set the 10s digit if greater, and not the last number
            if bank.cells[i] > tens_digit and i + 1 < len(bank.cells):
                tens_digit = bank.cells[i]
                ones_digit = bank.cells[i + 1]
            elif bank.cells[i] > ones_digit:
                # set the ones digit if greater
                ones_digit = bank.cells[i]

        return tens_digit * 10 + ones_digit

    @staticmethod
    def find_max_joltage_part_two_bf(bank: BatteryBank, num_to_activate: int) -> int:
        # find the max number between the last max and the end - remaining digits to find
        # so start 0 to len - 11, then found to len - 10
        # O(n * m), since we do m steps, over (about) n entries
        front = 0
        digits = [0] * num_to_activate
        # find to_activate digits
        for i in range(num_to_activate):
            # start from previous found, until the
            max_digit = 0

            # Ensure that you always pick a number before the required number to fill out a full answer
            for j in range(front, len(bank.cells) - num_to_activate + i + 1):
                if bank.cells[j] > max_digit:
                    max_digit = bank.cells[j]
                    digits[i] = max_digit
                    # Reduce the scope of the search from the next onward
                    front = j + 1

        return list_to_int(digits)

    @staticmethod
    def find_max_joltage_part_two_linear(
        bank: BatteryBank, num_to_activate: int
    ) -> int:
        # find the max when activating a given number of cells
        # This greedy algorithm runs in O(n) time
        # It iterates across the bank, maintaining a linked list of the digits, and a cache of potentially out of order digits

        if not bank.cells:
            return 0

        head = ListNode(bank.cells[0])
        tail = head

        # cache which nodes have a value less than their follower
        removable_cells = []
        count = 1
        for cell in bank.cells[1:]:
            # insert new battery at the end
            tail.next = ListNode(cell)
            tail.next.prev = tail
            tail = tail.next
            if tail.prev.value < tail.value:
                removable_cells.append(tail.prev)

            # don't remove any until we have a full set of digits, but also don't count each iteration
            if count < num_to_activate:
                count += 1
                continue

            # remove the first node that is less than a following node
            try:
                to_remove = removable_cells.pop(0)
                # We are not tail here, as tail is not added to removable_cells
                if head == to_remove:
                    # if we are head, update it, and no additions to removable_cells are required
                    head = to_remove.next
                    head.prev = None
                else:
                    # Remove ourselves from the list
                    to_remove.next.prev = to_remove.prev
                    to_remove.prev.next = to_remove.next
                    # Check previous again in case it is now less than it's new next
                    if to_remove.prev.value < to_remove.next.value:
                        removable_cells.insert(0, to_remove.prev)
            except IndexError:
                # Remove newly added node last if removable_cells is empty
                tail = tail.prev
                tail.next = None

        return list_to_int(head)


def run() -> int:
    calc = JoltageCalculator(12)
    with open("input.txt", "r") as f:
        for line in f:
            if not line.strip():
                continue

            bank = BatteryBank.parse_bank(line.strip())
            calc.add_max_joltage(bank)

    return calc.total_joltage


if __name__ == "__main__":
    print(run())
