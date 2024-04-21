

import itertools
import math
from typing import Sequence


def solve_onesixthree(numbers: list[int]) -> set[str]:
    """Take 6 numbers, determine all the ways they can give 163.
    
    Numbers can be added, multiplied, subtracted, or divided to get 163.
    Can be an empty list.

    To start with we do a brute-force approach: we generate all possible
    permutations of the numbers, and then we generate all possible ways to
    combine them with the operators (including different orders of operation).
    We then evaluate each of these combinations and check if it equals 163.
    """
    # Preconditions
    assert len(numbers) == 6

    numbers = sorted(numbers)
    permutations = itertools.permutations(numbers)
    exps = set()
    for perm in permutations:
        out = ops_and_perms(perm)
        if out is not None and out not in exps:
            print(out)
            exps.add(out)
    
    return exps

    
def ops_and_perms(perm: Sequence[int]) -> str | None:
    for ops in itertools.product("+-*/", repeat=5):
        # Generate all possible ways to combine the numbers with the operators
        # (including different orders of operation)
        expression = f"{perm[0]}{ops[0]}{perm[1]}{ops[1]}{perm[2]}{ops[2]}{perm[3]}{ops[3]}{perm[4]}{ops[4]}{perm[5]}"
        try:
            # try all the different ways of bracketing the expression
            result = eval(expression)
        except ZeroDivisionError:
            continue
        if math.isclose(result, 163):
            return expression
    return None

if __name__ == "__main__":
    # solve_onesixthree([1,2,3,4,5,6])
    solve_onesixthree([1, 5, 5, 8, 8, 13])