import typing as t
from pathlib import Path

from helpers.geometry import COORD, iter_neighbors
from helpers.parsing import parse_map_objects

LETTER_MAP_T: t.TypeAlias = dict[str, set[COORD]]
LETTER_COORDS_T: t.TypeAlias = dict[COORD, str]


def parse_word_search(raw_puzzle: str) -> tuple[LETTER_MAP_T, LETTER_COORDS_T]:
    """
    Parse the small Elf's word search and extract the letter locations.

    The provided word search is assumed to only contain the uppercase letters `X`, `M`, `A`, or `S`.
    All other characters are ignored.

    Letter locations are provided in two ways:
        * A per-letter mapping of letter coordinates
        * A mapping of coordinates to character contents
    """
    letter_map: LETTER_MAP_T = {letter: set() for letter in {"X", "M", "A", "S"}}
    letter_coords: dict[COORD, str] = {}
    for coord, c in parse_map_objects(raw_puzzle):
        if c in letter_map:
            letter_map[c].add(coord)
            letter_coords[coord] = c

    return letter_map, letter_coords


def count_word(
    letter_map: LETTER_MAP_T, letter_coords: LETTER_COORDS_T, query: str = "XMAS"
) -> int:
    """
    Count the occurrences of the provided query word in the provided parsed word search.

    Word queries must be at least 2 letters long and contain only the letters the uppercase letters
    `X`, `M`, `A`, or `S`, though this isn't enforced at all because this is fun puzzle time.

    The word search allows words to be horizontal, vertical, diagonal, written backwards, or even
    overlapping other words. As in a traditional word search, the word must be continuous along one
    of these directions to be considered.
    """
    n_occurrences = 0
    start_coords = letter_map[query[0]]
    for sc in start_coords:
        for n in iter_neighbors(sc, include_diagonal=True):
            if n in letter_map[query[1]]:
                dx, dy = (n[0] - sc[0], n[1] - sc[1])
                potential_word_c = [(sc[0] + (i * dx), sc[1] + (i * dy)) for i in range(len(query))]

                if all(((c in letter_coords) for c in potential_word_c)):
                    word = "".join(letter_coords[c] for c in potential_word_c)
                    if word == query:
                        n_occurrences += 1

    return n_occurrences


def count_x_mas(letter_map: LETTER_MAP_T, letter_coords: LETTER_COORDS_T) -> int:
    """
    Count the number of X-MAS occurrences in the provided parsed word search.

    An X-MAS is two MAS in the shape of an X, e.g.:

    ```
    M.S
    .A.
    M.S
    ```

    X-MASes may be found in any orientation as long as the X shape is retained.
    """
    raise NotImplementedError


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    letter_map, letter_coords = parse_word_search(puzzle_input)

    print(f"Part One: {count_word(letter_map, letter_coords)}")
    print(f"Part Two: {...}")
