from __future__ import annotations

from pprint import pprint
from dataclasses import dataclass
import math
from typing import Sequence


def solve_onesixthree(numbers: Sequence[int]) -> list[str]:
    """Take 6 numbers, determine all the ways they can give 163.
    
    Numbers can be added, multiplied, subtracted, or divided to get 163.
    Can be an empty list.

    We build binary trees of all possible ways to combine the numbers
    with the operators (including different orders of operation).
    We then evaluate each of these trees and check if it equals 163.
    """
    sols = []
    generated_trees = generate_trees(tuple(numbers))
    for tree in generated_trees:
        if math.isclose(tree.eval(), 163):
            sols.append(tree.elements[0].history)
    return sols

def plus(x: float, y: float) -> float:
    return x + y

def minus(x: float, y: float) -> float:
    return x - y

def times(x: float, y: float) -> float:
    return x * y

def divide(x: float, y: float) -> float | None:
    if y == 0:
        return None
    return x / y

def reverse_divide(x: float, y: float) -> float | None:
    if x == 0:
        return None
    return y / x
OPERATIONS = {
    "plus": plus,
    "minus": minus,
    "times": times,
    "divide": divide,
    "reverse_divide": reverse_divide,
}
@dataclass
class Element:
    value: float
    history: str = ""

    def __post_init__(self):
        if self.history == "":
            self.history = str(self.value)

@dataclass
class Tree:
    elements: tuple[Element, ...]
    def generate_children(self) -> list[Tree]:
        """Produce all possible trees with one fewer element."""
        # Pick two elements and an operator, and combine them
        children = []
        if len(self.elements) == 2:
            # If we only have two elements, we can only combine them
            for op in OPERATIONS:
                new_value = OPERATIONS[op](self.elements[0].value, self.elements[1].value)
                if new_value is None:
                    continue
                new_history = f"({self.elements[0].history} {op} {self.elements[1].history})"
                new_elements = tuple([Element(new_value, new_history)])
                children.append(Leaf(new_elements))
            return children
    
        # If we have more than two elements, we can combine any two of them
        for i in range(len(self.elements)):
            for j in range(i + 1, len(self.elements)):
                for op in OPERATIONS:
                    new_value = OPERATIONS[op](self.elements[i].value, self.elements[j].value)
                    if new_value is None:
                        continue
                    new_element = Element(new_value, f"({self.elements[i].history} {op} {self.elements[j].history})")
                    # new elements is all the elements except i and j, plus new_value
                    new_elements = tuple(self.elements[:i] + self.elements[i+1:j] + self.elements[j+1:] + (new_element,))
                    children.append(Tree(new_elements))
        return children

def generate_trees(numbers: tuple[int, ...]) -> list[Leaf]:
    """Generate all possible leaf nodes from the numbers."""
    leaves = []
    root = Tree(tuple(Element(n) for n in numbers))
    # DFS search
    queue = [root]
    while len(queue) > 0:
        current = queue.pop()
        children = current.generate_children()
        for child in children:
            if len(child.elements) == 1:
                leaves.append(child)
            else:
                queue.append(child)
    return leaves


class Leaf(Tree):
    def __post_init__(self):
        assert len(self.elements) == 1
    
    def eval(self) -> float:
        return self.elements[0].value

    
if __name__ == "__main__":
    # pprint(solve_onesixthree((1,2,3,4,5,6)))
    # print(solve_onesixthree((1,1,1,2,8,10)))
    # print(solve_onesixthree((3,16,10)))
    print(solve_onesixthree([1, 5, 5, 8, 8, 13]))