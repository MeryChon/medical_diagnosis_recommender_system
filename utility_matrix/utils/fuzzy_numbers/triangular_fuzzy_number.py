class TriangularFuzzyNumber(object):
    def __init__(self, a1=None, a2=None, a3=None):
        self.a1 = round(a1, 2) if a1 else 0
        self.a2 = round(a2, 2) if a2 else 0
        self.a3 = round(a3, 2) if a3 else 0

    def __add__(self, other):
        return TriangularFuzzyNumber(self.a1 + other.a1, self.a2 + other.a2, self.a3 + other.a3)

    def __str__(self):
        return f"({self.a1}, {self.a2}, {self.a3})"

    def __gt__(self, other):
        return self.a2 > self.a2

    def __ge__(self, other):
        return other.a2 >= self.a2

    def __lt__(self, other):
        return other.a2 < self.a2

    def __le__(self, other):
        return other.a2 <= self.a2

    def __round__(self, n=None):
        return TriangularFuzzyNumber(round(self.a1, n), round(self.a2, n), round(self.a3, n))

    def multiply_by_const(self, c):
        return TriangularFuzzyNumber(c * self.a1, c * self.a2, c * self.a3)

    def to_list(self):
        return [self.a1, self.a2, self.a3]
