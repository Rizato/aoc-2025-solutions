import enum
from typing import List


class Tile(enum.Enum):
    EMPTY = "."
    SPLITTER = "^"
    SOURCE = "S"
    BEAM = "|"


class TachyonField:
    """
    Maintains the current state of tachyon beams in a list
    For each line, it updates the current state based on the found items
    """

    def __init__(self, field: List[List[Tile]]):
        self.field: List[List[Tile]] = field
        self.width = len(field[0])
        self.current_state: List[Tile] = [Tile.EMPTY] * self.width

    def solve(self) -> int:
        splits = 0
        for row in self.field:
            for i, tile in enumerate(row):
                current = self.current_state[i]
                if tile == Tile.SOURCE:
                    self.current_state[i] = Tile.BEAM
                elif tile == Tile.SPLITTER:
                    if current == Tile.BEAM:
                        splits += 1
                        # beam stops, and moves left and right, if possible
                        self.current_state[i] = Tile.SPLITTER
                        if i > 0 and row[i - 1] != Tile.SPLITTER:
                            self.current_state[i - 1] = Tile.BEAM
                        if i < self.width - 1 and row[i + 1] != Tile.SPLITTER:
                            self.current_state[i + 1] = Tile.BEAM
                else:
                    # NOP
                    pass

        return splits


class TachyonParser:

    @staticmethod
    def parse(tachyon_field: str) -> TachyonField:
        rows = []
        for line in tachyon_field.splitlines():
            if not line.strip():
                continue
            row = []
            for tile in line:
                row.append(Tile(tile))
            rows.append(row)

        return TachyonField(rows)


def run() -> int:

    with open("input.txt", "r") as f:
        tachyon_field = TachyonParser().parse(f.read())

    return tachyon_field.solve()


if __name__ == "__main__":
    print(run())
