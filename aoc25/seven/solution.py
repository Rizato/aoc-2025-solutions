import enum
from functools import lru_cache
from typing import List


class Tile(enum.Enum):
    EMPTY = "."
    SPLITTER = "^"
    SOURCE = "S"
    BEAM = "|"


class TreeNode:

    def __init__(self):
        self.left = None
        self.right = None


@lru_cache(maxsize=None)
def count_paths(root: TreeNode):
    if not root:
        return 0

    if not root.left and not root.right:
        return 1
    else:
        return count_paths(root.left) + count_paths(root.right)


class TachyonField:
    """
    Maintains the current state of tachyon beams in a list
    For each line, it updates the current state based on the found items
    """

    def __init__(self, field: List[List[Tile]]):
        self.field: List[List[Tile]] = field
        self.width = len(field[0])

    def solve(self) -> int:
        splits = 0
        previous_state = [Tile.EMPTY] * self.width
        for row in self.field:
            next_state = [Tile.EMPTY] * self.width
            for i, tile in enumerate(row):
                if tile == Tile.SOURCE:
                    next_state[i] = Tile.BEAM
                elif tile == Tile.SPLITTER:
                    next_state[i] = Tile.SPLITTER
                    if previous_state[i] == Tile.BEAM:
                        splits += 1
                        for j in (i - 1, i + 1):
                            # beam stops, and moves left and right, if possible
                            if 0 <= j < self.width and row[j] != Tile.SPLITTER:
                                next_state[j] = Tile.BEAM

                else:  # tile is empty
                    next_state[i] = (
                        previous_state[i]
                        if previous_state[i] == Tile.BEAM
                        else next_state[i]
                    )

            previous_state = next_state
        return splits

    def solve_quantum_paths(self) -> int:
        root = TreeNode()
        current_state: List[List[TreeNode]] = [list() for _ in range(self.width)]
        # Find source
        source = self.field[0].index(Tile.SOURCE)
        current_state[source].append(root)
        for row in self.field[1:]:
            # find all splitters, with TreeNodes in current_state
            splitters = [
                i
                for i, tile in enumerate(row)
                if tile == Tile.SPLITTER and current_state[i]
            ]
            # create a new node per new path, using set to remove dupes
            tachyon_splits = {j for i in splitters for j in (i - 1, i + 1)}
            for j in tachyon_splits:
                tachyon = TreeNode()
                if 0 <= j < self.width:
                    current_state[j].append(tachyon)
                    # Add a node to all parents in the state (from earlier splits leading to the same path)
                    parent_left = j - 1
                    if parent_left in splitters:
                        for parent in current_state[parent_left]:
                            # parent left, has this child in right slot
                            parent.right = tachyon
                    parent_right = j + 1
                    if parent_right in splitters:
                        for parent in current_state[parent_right]:
                            parent.left = tachyon
            for i in splitters:
                # remove all the splitters, so they don't get split again
                current_state[i].clear()

        return count_paths(root)


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

    return tachyon_field.solve_quantum_paths()


if __name__ == "__main__":
    print(run())
