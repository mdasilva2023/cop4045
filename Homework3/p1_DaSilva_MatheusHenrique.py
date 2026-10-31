"""Homework 3, Problem 1 - Matheus Henrique Da Silva - Z23704669"""

from numbers import Real
from testif import testif


class NVector:
    """represent an N-dimensional vector of real numbers stored in a list."""

    def __init__(self, *values: Real | list[Real] | tuple[Real, ...]) -> None:
        """create a vector from a list, tuple, or individual real numbers.

        needs at least one argument and real-number elements.
        the input sequence is copied to prevent accidental aliasing.
        """
        if len(values) == 1 and isinstance(values[0], (list, tuple)):
            elements = list(values[0])
        else:
            elements = list(values)
        if not all(isinstance(value, Real) for value in elements):
            raise TypeError("All vector elements must be real numbers")
        self.elements: list[Real] = elements

    def __len__(self) -> int:
        """return the dimension of this vector."""
        return len(self.elements)

    def __getitem__(self, index: int) -> Real:
        """return the element at index; supports negative integer indices."""
        return self.elements[index]

    def __setitem__(self, index: int, value: Real) -> None:
        """replace the element at index with a real number."""
        if not isinstance(value, Real):
            raise TypeError("Vector elements must be real numbers")
        self.elements[index] = value

    def __str__(self) -> str:
        """return a readable representation of the vector."""
        return f"NVector({self.elements})"

    def __eq__(self, other: object) -> bool:
        """return True when other is an NVector with identical elements."""
        return isinstance(other, NVector) and self.elements == other.elements

    def __ne__(self, other: object) -> bool:
        """return True when other is not equal to this vector."""
        return not self.__eq__(other)

    def __add__(self, other: 'NVector | Real') -> 'NVector':
        """return element-wise vector addition or addition of a real scalar.

        both vectors must have the same dimension.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vector dimensions must match")
            return NVector([a + b for a, b in zip(self.elements, other.elements)])
        if isinstance(other, Real):
            return NVector([a + other for a in self.elements])
        return NotImplemented

    def __radd__(self, other: Real) -> 'NVector':
        """Support addition when a real scalar is on the left."""
        return self.__add__(other)

    def __mul__(self, other: 'NVector | Real') -> Real:
        """return a dot product with a vector or scalar times the element sum.

        dot products require vectors of equal dimension.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vector dimensions must match")
            return sum(a * b for a, b in zip(self.elements, other.elements))
        if isinstance(other, Real):
            return sum(a * other for a in self.elements)
        return NotImplemented

    def __rmul__(self, other: Real) -> Real:
        """support multiplication when a real scalar is on the left."""
        return self.__mul__(other)

    @classmethod
    def zeros(cls, n: int) -> 'NVector':
        """return a new vector with n zeros; n must be nonnegative integer."""
        if not isinstance(n, int):
            raise TypeError("Dimension must be an integer")
        if n < 0:
            raise ValueError("Dimension cannot be negative")
        return cls([0] * n)



def main() -> None:
    """test the NVector methods using the Homework 3 testif function."""
    print("Homework 3 - Problem 1: NVector Tests - Matheus Henrique Da Silva - Z23704669")
    v = NVector(3, 0, 1, -1)
    w = NVector([1, 2, 3, 4])
    testif(v == NVector([3, 0, 1, -1]), "Constructor", "Constructor works", "Constructor failed")
    testif(len(v) == 4, "Length", "Length works", "Length failed")
    testif(v[0] == 3 and v[-1] == -1, "Indexing", "Indexing works", "Indexing failed")
    v[2] = 5
    testif(v[2] == 5, "Setitem", "Setitem works", "Setitem failed")
    testif(str(v) == "NVector([3, 0, 5, -1])", "String", "String works", "String failed")
    testif(v != w and v == NVector(3, 0, 5, -1), "Comparison", "Comparison works", "Comparison failed")
    testif(v + w == NVector(4, 2, 8, 3), "Vector addition", "Vector addition works", "Vector addition failed")
    testif(v + 10 == NVector(13, 10, 15, 9), "Scalar addition", "Scalar addition works", "Scalar addition failed")
    testif(10 + v == NVector(13, 10, 15, 9), "Reflected addition", "Reflected addition works", "Reflected addition failed")
    testif(v * w == 14, "Dot product", "Dot product works", "Dot product failed")
    testif(v * 2 == 14, "Scalar multiplication", "Scalar multiplication works", "Scalar multiplication failed")
    testif(2 * v == 14, "Reflected multiplication", "Reflected multiplication works", "Reflected multiplication failed")
    testif(NVector.zeros(4) == NVector(0, 0, 0, 0), "Zeros", "Zeros works", "Zeros failed")
    original = [1, 2, 3]
    copied = NVector(original)
    original[0] = 99
    testif(copied[0] == 1, "Independent list copy", "Independent list copy works", "Independent list copy failed")


if __name__ == "__main__":
    main()
