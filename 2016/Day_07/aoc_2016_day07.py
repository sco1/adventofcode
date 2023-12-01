from pathlib import Path

import more_itertools as miter


def is_abba(substr: str) -> bool:
    """
    Determine if the provided substring is an Autonomous Bridge Bypass Annotation (ABBA).

    An ABBA is any four-character sequence which consists of a pair of two different characters
    followed by the reverse of that pair, e.g. `xyyx` or `abba`.
    """
    if len(substr) != 4:
        raise ValueError(f"Substring must be of length 4. Received: {len(substr)}")

    if substr[0] == substr[1]:
        # Interior characters must be different
        return False

    return substr[:2] == substr[-1:1:-1]


def has_abba(substr: str) -> bool:
    """
    Determine if the provided substring has at least one Autonomous Bridge Bypass Annotation (ABBA).

    An ABBA is any four-character sequence which consists of a pair of two different characters
    followed by the reverse of that pair, e.g. `xyyx` or `abba`.
    """
    if len(substr) < 4:
        raise ValueError(f"Substring must have at least 4 characters. Received {len(substr)}")

    return any(is_abba("".join(chunk)) for chunk in miter.windowed(substr, 4, fillvalue=""))


def parse_ip(address: str) -> tuple[list[str], list[str]]:
    """
    Parse the IP into its component substrings.

    IP addresses are assumed to be of the form `<supernet>[<hypernet>]`, where each address can
    have one or more of both supernets and hypernets.
    """
    supernets = []
    hypernets = []

    buffer: list[str] = []
    for c in address:
        if c == "[":
            supernets.append("".join(buffer))
            buffer.clear()
        elif c == "]":
            hypernets.append("".join(buffer))
            buffer.clear()
        else:
            buffer.append(c)
    else:
        if buffer:
            supernets.append("".join(buffer))

    return supernets, hypernets


def supports_tls(address: str) -> bool:
    """
    Determine if the provided IP address supports TLS.

    An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA. An ABBA is any
    four-character sequence which consists of a pair of two different characters followed by the
    reverse of that pair, such as `xyyx` or `abba`. However, the IP also must not have an ABBA
    within any hypernet sequences, which are contained by square brackets.
    """
    supernets, hypernets = parse_ip(address)

    # Check hypernet first since it's a disqualifier
    if any(has_abba(h) for h in hypernets):
        return False

    return any(has_abba(c) for c in supernets)


def is_aba(substr: str) -> bool:
    """
    Determine if the provided substring is an Area-Broadcast Accessor (ABA).

    An ABA is any three-character sequence which consists of the same character twice with a
    different character between them, such as `xyx` or `aba`.
    """
    if len(substr) != 3:
        raise ValueError(f"Substring must be of length 3. Received: {len(substr)}")

    if (substr[0] != substr[2]) or (substr[0] == substr[1]):
        return False
    else:
        return True


def calculate_bab(aba: str) -> str:
    """
    Calculate the BAB that corresponds to the given ABA.

    The corresponding BAB for a given ABA is calculated using the characters in reversed positions,
    e.g. `xyx` becomes `yxy`.
    """
    if len(aba) != 3:
        raise ValueError(f"Substring must be of length 3. Received: {len(aba)}")

    return f"{aba[1]}{aba[0]}{aba[1]}"


def supports_ssl(address: str) -> bool:
    """
    Determine if the provided IP address supports SSL.

    An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in the supernet
    sequences (outside any square bracketed sections), and a corresponding Byte Allocation Block,
    or BAB, anywhere in the hypernet sequences. An ABA is any three-character sequence which
    consists of the same character twice with a different character between them, such as `xyx` or
    `aba`. A corresponding BAB is the same characters but in reversed positions: `yxy` and `bab`,
    respectively.
    """
    supernets, hypernets = parse_ip(address)
    for snet in supernets:
        for chunk in miter.windowed(snet, 3, fillvalue=""):
            substr = "".join(chunk)
            if is_aba(substr):
                bab = calculate_bab(substr)
                if any(bab in hnet for hnet in hypernets):
                    return True

    return False


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {sum(supports_tls(ip) for ip in puzzle_input.splitlines())}")
    print(f"Part Two: {sum(supports_ssl(ip) for ip in puzzle_input.splitlines())}")
