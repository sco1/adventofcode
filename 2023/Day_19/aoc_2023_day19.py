from __future__ import annotations

import operator
from collections import abc
from dataclasses import astuple, dataclass
from functools import partial
from pathlib import Path


@dataclass
class Part:  # noqa: D101
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_raw(cls, raw_part: str) -> Part:
        """
        Generate a `Part` instance from the provided specification string.

        Part strings are assumed to be of the form `{x=787,m=2655,a=1222,s=2876}`, and parameters
        are assumed to always be in `x, m, a, s` order.
        """
        raw_part = raw_part.strip("{}")
        digits = [int(chunk.split("=")[-1]) for chunk in raw_part.split(",")]
        return cls(*digits)


def _comp(part: Part, part_attr: str, oper: abc.Callable, comp_val: int) -> bool:
    return oper(operator.attrgetter(part_attr)(part), comp_val)


def _find_operator(raw_str: str) -> abc.Callable[[Part], bool] | None:
    """
    Create a partial function for the provided predicate conditional.

    The returned partial function accepts a `Part` instance and performs the specified comparison;
    currently only `<` and `>` are accepted.

    For example, `"a>1716"` will provide a partial function `f`, where `f(Part)` executes the
    `Part.a > 1716` comparison and returns its boolean result.
    """
    if "<" in raw_str:
        left, right = raw_str.split("<")
        return partial(_comp, part_attr=left, oper=operator.lt, comp_val=int(right))
    elif ">" in raw_str:
        left, right = raw_str.split(">")
        return partial(_comp, part_attr=left, oper=operator.gt, comp_val=int(right))
    else:
        return None


@dataclass
class Conditional:
    """
    Representation of a workflow's conditional chain.

    A workflow may be composed of multiple conditionals; the `if_true` path always results in a
    bin destination (as `str`), but the `if_false` path may map to either an additional conditional
    or a bin destination.
    """

    predicate: abc.Callable[[Part], bool]
    if_true: str
    if_false: Conditional | str

    def filter_part(self, part: Part) -> str:
        """Follow the conditional chain for the specified part and output its destination bin."""
        if self.predicate(part):
            return self.if_true
        else:
            if isinstance(self.if_false, str):
                return self.if_false
            else:
                return self.if_false.filter_part(part)

    @classmethod
    def from_raw(cls, raw_instruction: str) -> Conditional:
        """
        Generate a `Conditional` instance from the provided raw instruction statement.

        Statements are of the form `a<2006:qkq,m>2090:A,rfg`, which is a comma-separated flow of
        conditionals for a given part. The flow of the example string is as follows:
            * If `a<2006`, the destination bin is `qkq`
            * Otherwise, if `m>2090`, the destination bin is `A`
            * Otherwise, the destination bin is `rfg`
        """
        raw_predicate, *follows = raw_instruction.split(",")
        raw_cond, if_true = raw_predicate.split(":")
        pred_op = _find_operator(raw_cond)

        if pred_op is None:
            raise ValueError(f"Could not parse conditional statement: '{raw_predicate}'")

        if len(follows) > 1:
            return Conditional(
                predicate=pred_op, if_true=if_true, if_false=Conditional.from_raw(",".join(follows))
            )
        else:
            return Conditional(predicate=pred_op, if_true=if_true, if_false=follows[0])


def parse_instructions(raw_instructions: str) -> tuple[dict[str, Conditional], list[Part]]:
    """
    Parse the specified instruction mapping into its workflow and part components.

    The instruction begins with one or more lines of workflow specifications, of the form understood
    by `Conditional.from_raw`, followed by a blank line, then one or more lines of part
    specifications, of the fowm understood by `Part.from_raw`.
    """
    raw_workflows, raw_parts = raw_instructions.split("\n\n")
    workflows = {}
    for rw in raw_workflows.splitlines():
        workflow_id, raw_flow = rw.split("{")
        raw_flow = raw_flow.strip("{}")
        workflows[workflow_id] = Conditional.from_raw(raw_flow)

    parts = [Part.from_raw(line) for line in raw_parts.splitlines()]

    return workflows, parts


def sort_parts(parts: abc.Iterable[Part], workflows: dict[str, Conditional]) -> list[Part]:
    """
    Pass each part through the specified workflow(s) and return a list of accepted parts.

    Parts are assumed to pass through the workflows until they terminate in either the bin marked
    `A`, for accepted, or `R`, for rejected. It is assumed that no workflows pull from either one of
    these terminal bins.
    """
    accepted = []
    for p in parts:
        current_bin = workflows["in"].filter_part(p)
        while True:
            if current_bin == "A":
                accepted.append(p)
                break

            current_bin = workflows[current_bin].filter_part(p)

    return accepted


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    workflows, parts = parse_instructions(puzzle_input)
    accepted_parts = sort_parts(parts, workflows)
    print(f"Part One: {sum(sum(astuple(p)) for p in accepted_parts)}")
    print(f"Part Two: {...}")
