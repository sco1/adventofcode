import argparse
from pathlib import Path
from string import Template

from helpers.common import validate_puzzle_date

BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = Path(__file__).parent / "templates"
TEMPLATE_SUFFIX = ".tmpl"

# Shared across all languages; created empty if not already present
PUZZLE_FILES = (
    "puzzle_input.txt",
    "README.md",
)


def available_langs() -> list[str]:
    """Return the languages that have a template folder, sorted by name."""
    return sorted(p.name for p in TEMPLATE_DIR.iterdir() if p.is_dir())


def render_lang(lang: str, year: int, day: int) -> dict[Path, str]:
    """
    Render the template files for `lang`, returning a mapping of day-relative paths to contents.

    Template paths and contents are `string.Template` strings, with `${year}` substituted as the
    4-digit year and `${day}` substituted as the zero-padded 2-digit day. The `.tmpl` suffix is
    stripped from each template's filename.
    """
    lang_dir = TEMPLATE_DIR / lang
    mapping = {"year": f"{year}", "day": f"{day:02d}"}

    rendered = {}
    for template in sorted(lang_dir.rglob(f"*{TEMPLATE_SUFFIX}")):
        rel_path = template.relative_to(lang_dir).as_posix().removesuffix(TEMPLATE_SUFFIX)
        out_path = Path(Template(rel_path).substitute(mapping))
        rendered[out_path] = Template(template.read_text()).substitute(mapping)

    return rendered


def init_puzzle_day(year: int, day: int, langs: list[str]) -> list[Path]:
    """
    Create the puzzle folder for the given year & day, populated with templates for `langs`.

    The day folder may already exist, allowing a language to be added to a day that was previously
    initialized. Existing files are never overwritten: if any language template would clobber an
    existing file, a `FileExistsError` is raised before anything is written.

    Returns the paths of the files that were created.
    """
    day_dir = BASE_DIR / f"{year}" / f"Day_{day:02d}"

    to_write: dict[Path, str] = {}
    for lang in langs:
        for rel_path, contents in render_lang(lang, year, day).items():
            to_write[day_dir / rel_path] = contents

    conflicts = sorted(p for p in to_write if p.exists())
    if conflicts:
        conflict_list = "\n".join(f"  {p.relative_to(BASE_DIR).as_posix()}" for p in conflicts)
        raise FileExistsError(f"Refusing to overwrite existing files:\n{conflict_list}")

    created = []
    for filename in PUZZLE_FILES:
        puzzle_file = day_dir / filename
        if not puzzle_file.exists():
            puzzle_file.parent.mkdir(parents=True, exist_ok=True)
            puzzle_file.touch()
            created.append(puzzle_file)

    for path, contents in to_write.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents)
        created.append(path)

    return created


def main() -> None:  # noqa: D103
    langs = available_langs()

    parser = argparse.ArgumentParser(description="Initialize an Advent of Code puzzle day folder.")
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    parser.add_argument(
        "--lang",
        nargs="+",
        choices=langs,
        default=["python"],
        help="Language template(s) to create (default: python)",
    )

    args = parser.parse_args()
    try:
        validate_puzzle_date(args.year, args.day)
    except ValueError as e:
        parser.error(str(e))

    try:
        created = init_puzzle_day(args.year, args.day, args.lang)
    except FileExistsError as e:
        parser.exit(1, f"{e}\n")

    for path in created:
        print(f"Created {path.relative_to(BASE_DIR).as_posix()}")


if __name__ == "__main__":
    main()
