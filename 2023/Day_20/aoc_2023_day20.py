from __future__ import annotations

from collections import abc, defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Signal:  # noqa: D101
    origin: str
    destination: str
    value: bool

    def __str__(self) -> str:
        if self.value:
            state = "high"
        else:
            state = "low"
        return f"{self.origin} -{state}-> {self.destination}"


@dataclass
class Module:
    """
    Communication module base class.

    Child classes should implement `process` that accepts an incoming `Signal` and, if necessary,
    yields an output `Signal` to all destination modules.
    """

    name: str
    destinations: list[Module] = field(default_factory=list)

    sent_low: int = 0
    sent_high: int = 0

    def _increment_sent(self, signal: bool) -> None:
        if signal:
            self.sent_high += 1
        else:
            self.sent_low += 1

    def _reset(self) -> None:
        self.sent_low = self.sent_high = 0

    def process(self, signal: Signal) -> abc.Generator[Signal, None, None]:  # noqa: D102
        raise NotImplementedError


@dataclass
class FlipFlop(Module):
    """
    Flip-flop module (`%`) representation.

    Flip-flop modules are either on or off; they are initially off. If a flip-flop module receives a
    high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low
    pulse, it flips between on and off. If it was off, it turns on and sends a high pulse. If it was
    on, it turns off and sends a low pulse.
    """

    state: bool = False

    def process(self, signal: Signal) -> abc.Generator[Signal, None, None]:  # noqa: D102
        if not signal.value:
            self.state = not self.state
            out_signal = self.state
            for d in self.destinations:
                self._increment_sent(out_signal)
                yield Signal(self.name, d.name, out_signal)


@dataclass
class Conjunction(Module):
    """
    Conjunction module (`&`) representation.

    Conjunction modules remember the type of the most recent pulse received from each of their
    connected input modules; they initially default to remembering a low pulse for each input. When
    a pulse is received, the conjunction module first updates its memory for that input. Then, if it
    remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
    """

    state: dict[str, bool] = field(default_factory=dict)

    def process(self, signal: Signal) -> abc.Generator[Signal, None, None]:  # noqa: D102
        self.state[signal.origin] = signal.value
        out_signal = not all(self.state.values())
        for d in self.destinations:
            self._increment_sent(out_signal)
            yield Signal(self.name, d.name, out_signal)


@dataclass
class Broadcaster(Module):
    """
    Broadcast module representation.

    When the broadcast module receives a pulse, it sends the same pulse to all of its destination
    modules.
    """

    def process(self, signal: Signal) -> abc.Generator[Signal, None, None]:  # noqa: D102
        for d in self.destinations:
            self._increment_sent(signal.value)
            yield Signal(self.name, d.name, signal.value)


@dataclass
class Dump(Module):
    """
    Null module representation.

    This module receives a signal and does nothing.
    """

    def process(self, signal: Signal) -> abc.Generator[Signal, None, None]:  # noqa: D102
        pass


def parse_module_configuration(config: str) -> dict[str, Module]:
    """
    Parse the provided module configuration into its components.

    Each line of the module configuration lists a module and its output connections, in the form:
    `<module> -> <connections>`, where connections is a comma separated list of one or more
    connected modules. The module name is preceded by a symbol identifying its type, if any;
    flip-flop modules have the prefix `%` and conjunction modules have the prefix `&`. It is assumed
    that only one special untyped module, `broadcaster` is present, representing the broadcast
    module.

    For example:
        * `broadcaster -> a, b, c` is a broadcast module connected to `a`, `b`, and `c`
        * `%a -> b` is a flip-flop module connected to `b`
        * `&inv -> a, b` is a conjunction module connected to `a` and `b`

    If a module is listed as an output connection but does not have a specification line in the
    configuration string, it is considered a null module, which receives input and sends nothing.
    """
    modules: dict[str, Module] = {}
    staging = {}  # stage output wiring until all modules are initialized
    # Track incoming connections for each conjunction module
    conjunctions: dict[str, list[str]] = defaultdict(list)
    for line in config.splitlines():
        module_name, raw_destinations = (c.strip() for c in line.split("->"))
        destinations = [c.strip() for c in raw_destinations.split(",")]

        if module_name == "broadcaster":
            modules["broadcaster"] = Broadcaster(name=module_name)
        else:
            prefix = module_name[0]
            module_name = module_name[1:]
            if prefix == "%":
                modules[module_name] = FlipFlop(name=module_name)
            elif prefix == "&":
                modules[module_name] = Conjunction(name=module_name)
                conjunctions[module_name] = []
            else:
                raise ValueError(f"Unknown prefix: '{prefix}'")

        staging[module_name] = destinations

    # Wire up destination modules
    for parent, destinations in staging.items():
        dms = []
        for d in destinations:
            # If we see a destination that isn't specced, create a null module for it
            if d not in modules:
                modules[d] = Dump(name=d)
            dms.append(modules[d])

            # Track incoming conjunction connections to initialize their internal state
            if isinstance(modules[d], Conjunction):
                conjunctions[d].append(parent)

        modules[parent].destinations = dms

    # Initialize conjunction internal state
    for conj_name, incoming in conjunctions.items():
        # If we're accessing a module here then we know it's a conjunction module
        modules[conj_name].state = {s: False for s in incoming}  # type: ignore[attr-defined]

    return modules


def press_button(modules: dict[str, Module], n_presses: int = 1000) -> int:
    """
    Press the big red button n times & simulate the communications signal process until completion.

    For each button press, a low pulse is sent to the broadcast module, beginning the signal chain.
    After pushing the button, all pulses are processed in the order they are sent. It is assumed
    that the signal chain completes after each button press and does not contain any cycles.

    Each module, including the button, keeps track of the number of low and high pulses sent. Upon
    completion of all button presses, the total number of low pulses sent and total number of high
    pulses sent are multiplied together and returned.
    """
    # Reset module state
    for m in modules.values():
        m._reset()

    for _ in range(n_presses):
        signal_queue: deque[Signal] = deque()
        signal_queue.append(Signal("button", "broadcaster", False))
        while signal_queue:
            signal = signal_queue.popleft()
            if not isinstance(modules[signal.destination], Dump):
                signal_queue.extend(modules[signal.destination].process(signal))

    n_low = sum(m.sent_low for m in modules.values()) + n_presses  # Button adds 1 low signal
    n_high = sum(m.sent_high for m in modules.values())
    return n_low * n_high


def press_until_sand(modules: dict[str, Module]) -> int:
    """
    Count the number of button presses required until the `rx` module receives a low pulse.

    WARNING: This it not brute-force friendly!
    """
    if "rx" not in modules:
        raise ValueError("No 'rx' module found.")

    # Reset module state
    for m in modules.values():
        m._reset()

    n_presses = 0
    signal_queue: deque[Signal] = deque()
    while True:
        if not signal_queue:
            signal_queue.append(Signal("button", "broadcaster", False))
            n_presses += 1

        signal = signal_queue.popleft()
        if signal.destination == "rx" and not signal.value:
            return n_presses

        if not isinstance(modules[signal.destination], Dump):
            signal_queue.extend(modules[signal.destination].process(signal))


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    modules = parse_module_configuration(puzzle_input)
    print(f"Part One: {press_button(modules)}")
    print(f"Part Two: {press_until_sand(modules)}")
