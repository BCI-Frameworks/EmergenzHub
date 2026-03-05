from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Callable, Iterable, Iterator, Optional, Sequence, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class BruteForceResult(T):
    """
    Placeholder for type checkers; you can ignore this.
    """


def enumerate_fixed_length_sequences(
    alphabet: Sequence[T],
    length: int,
) -> Iterator[tuple[T, ...]]:
    """
    Exhaustively enumerates all sequences of exactly `length` over `alphabet`.
    Completeness: yields every element of S = alphabet^length exactly once.
    Termination: finite search space => iterator ends.
    """
    if length < 0:
        raise ValueError("length must be >= 0")
    if length > 0 and len(alphabet) == 0:
        # Empty alphabet yields empty search space for positive length
        return iter(())
    # itertools.product is a complete cartesian power enumeration
    return product(alphabet, repeat=length)


def brute_force_find(
    candidates: Iterable[T],
    predicate: Callable[[T], bool],
) -> Optional[T]:
    """
    Generic brute-force search:
    - Iterates all candidates in order
    - Returns first candidate satisfying predicate
    - Returns None if none match
    Correctness: if a matching element exists in `candidates`, it will be found.
    """
    for c in candidates:
        if predicate(c):
            return c
    return None


def brute_force_find_in_cartesian_power(
    alphabet: Sequence[T],
    length: int,
    predicate: Callable[[tuple[T, ...]], bool],
) -> Optional[tuple[T, ...]]:
    """
    Combined convenience function:
    - defines search space S = alphabet^length
    - enumerates S completely
    - applies predicate
    """
    return brute_force_find(
        enumerate_fixed_length_sequences(alphabet, length),
        predicate,
    )


# ---------------------------
# Minimal self-checks (sanity)
# ---------------------------
if __name__ == "__main__":
    # Completeness check: |alphabet^length| == len(alphabet)**length
    alphabet = ["A", "B", "C"]
    length = 4
    all_items = list(enumerate_fixed_length_sequences(alphabet, length))
    assert len(all_items) == len(alphabet) ** length
    assert len(set(all_items)) == len(all_items)  # uniqueness

    # Example predicate (purely local): find a specific tuple
    target = ("B", "A", "C", "A")
    found = brute_force_find_in_cartesian_power(
        alphabet,
        length,
        lambda tup: tup == target,
    )
    assert found == target
    print("OK")
