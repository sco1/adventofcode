import itertools
from collections import defaultdict
from pathlib import Path


def parse_terminal_session(session: list[str]) -> dict[str, int]:
    """
    Parse the provided terminal session output & calculate the directory tree sizes.

    The prompt is assumed to be `"$"`, and there are 2 commands currently supported:
        * `cd`, which accepts the following destinations:
            * `cd x` moves in one level
            * `cd ..` moves out one level
            * `cd /` moves to the outermost directory (root)
        * `ls`, which will print all of the files and directories immediately contained by the
        current directory:
            * `123 abc` means that the current directory contains a file named abc with size `123`
            * `dir xyz` means that the current directory contains a directory named `xyz`

    NOTE: It is assumed that `cd /` is the first command run in the provided output.
    """
    dir_sizes: dict[str, int] = defaultdict(int)
    for lineno, line in enumerate(session, start=1):
        match line.split():
            # Commands
            case ("$", "cd", "/"):
                # Move to outermost directory (root)
                loc = ["/"]
            case ("$", "cd", ".."):
                # Move out one level
                # This needs to be above the more generic cd so it doesn't get eaten
                loc.pop()
            case ("$", "cd", dest):
                # Move in one level
                loc.append(f"{dest}/")
            case ("$", "ls"):
                # No-op for our purposes, the next line(s) will show contents of the current dir
                continue

            # Output lines
            case ("dir", _):
                # No-op for our purposes, indicates a child directory
                continue
            case (printed_filesize, _):
                # File & its size, we only care about the filesize
                filesize = int(printed_filesize)

                # Since the total size of a directory is the sum of the sizes of the files it
                # contains, both directly and indirectly, we need to add this filesize to the
                # current location, as well as all of its parents, if they exist
                # accumulate is nice here since it takes care of our string slicing/joining for us
                # e.g. list(accumulate(["a", "b", "c"])) -> ['a', 'ab', 'abc']
                for path in itertools.accumulate(loc):
                    dir_sizes[path] += filesize
            case _:
                raise ValueError(f"Unrecognized ouput on line {lineno}")

    return dir_sizes


def calculate_candidate_dir_size(dir_sizes: dict[str, int], target: int = 100_000) -> int:
    """Calculate the total size of all directories whose size is at most `target`."""
    return sum(value for value in dir_sizes.values() if value <= target)


def find_best_deletion(
    dir_sizes: dict[str, int], system_size: int = 70_000_000, min_free: int = 30_000_000
) -> int:
    """Identify the smallest directory that can be deleted to free up enough space on the system."""
    threshold = dir_sizes["/"] - (system_size - min_free)
    return min(value for value in dir_sizes.values() if value >= threshold)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    dir_sizes = parse_terminal_session(puzzle_input)
    print(f"Part One: {calculate_candidate_dir_size(dir_sizes)}")
    print(f"Part Two: {find_best_deletion(dir_sizes)}")
