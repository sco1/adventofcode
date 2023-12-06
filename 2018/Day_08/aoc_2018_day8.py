from __future__ import annotations

from collections import abc, deque
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Node:  # noqa: D101
    header: tuple[int, int]
    children: list[Node]
    metadata: list[int]

    value: int = field(init=False)

    def __post_init__(self) -> None:
        """
        Calculate the value of the node.

        The value of a node depends on whether it has child nodes; if a node has no child nodes, its
        value is the sum of its metadata entries.

        If a node does have child nodes, the metadata entries become indexes which refer to those
        child nodes. A metadata entry of `1` refers to the first child node, `2` to the second, `3`
        to the third, and so on. The value of this node is the sum of the values of the child nodes
        referenced by the metadata entries. If a referenced child node does not exist, that
        reference is skipped. A child node can be referenced multiple time and counts each time it
        is referenced. A metadata entry of `0` does not refer to any child node.

        NOTE: It is assumed that if a node has children then it also has metadata entries.
        """
        if not self.children:
            self.value = sum(self.metadata)
            return

        self.value = 0
        for idx in self.metadata:
            try:
                # Metadata is 1-indexed
                self.value += self.children[idx - 1].value
            except IndexError:
                pass


def parse_license_file(license: str) -> Node:
    """Parse the provided license file into its tree representation."""
    license_vals = [int(n) for n in license.split()]
    tree, _ = parse_tree(license_vals)

    return tree


def parse_tree(vals: abc.Iterable[int]) -> tuple[Node, deque[int]]:
    """
    Create a tree representation of the provided license file values.

    The tree is made up of nodes; a single, outermost node forms the tree's root, and it contains
    all other nodes in the tree; nodes may be nested.

    A node consists of a header, which is always two numbers: the quantity of child nodes and the
    quantity of metadata entries. Following the header are zero or more child nodes and one or more
    metadata entries.
    """
    queue = deque(vals)
    n_children, n_metadata = (queue.popleft() for _ in range(2))

    children = []
    for _ in range(n_children):
        child, queue = parse_tree(queue)
        children.append(child)

    metadata = [queue.popleft() for _ in range(n_metadata)]

    return Node(header=(n_children, n_metadata), children=children, metadata=metadata), queue


def sum_tree_metadata(tree: Node) -> int:
    """Recurse through the given tree & sum the metadata values from all nodes."""
    queue = deque([tree])
    metadata_sum = 0
    while queue:
        node = queue.pop()
        metadata_sum += sum(node.metadata)

        queue.extend(node.children)

    return metadata_sum


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    tree = parse_license_file(puzzle_input)
    print(f"Part One: {sum_tree_metadata(tree)}")
    print(f"Part Two: {tree.value}")
