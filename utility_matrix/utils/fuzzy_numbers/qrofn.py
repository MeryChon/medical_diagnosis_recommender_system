import decimal

from utility_matrix.utils.fuzzy_numbers.interface import FuzzyNumber


class QROFN(FuzzyNumber):
    _score = None
    _accuracy = None

    def __init__(self, m=0, n=1, q=None):
        self.validate(m, n, q)
        self._m = self.to_decimal(m)
        self._n = self.to_decimal(n)
        if m and n:
            self._q = self.to_decimal(q) if q else QROFN.calculate_rung(self._m, self._n)
        else:
            self._q = 1
        self._score = self.calculate_score()
        self._accuracy = self.calculate_accuracy()
        super(QROFN, self).__init__(m, n, q)

    @property
    def m(self):
        return round(float(self._m), 3)

    @property
    def n(self):
        return round(float(self._n), 3)

    @property
    def q(self):
        return self._q

    @property
    def score(self):
        return round(float(self._score), 3)

    @property
    def accuracy(self):
        return round(float(self._accuracy), 3)

    def validate(self, m, n, q):
        if m < 0 or m > 1 or n < 0 or n > 1:
            raise ValueError("Membership grades must be positive numbers from [0, 1] interval")

        if q is not None and (not isinstance(q, int) or q < 0):
            raise ValueError("Rung must be a positive integer")

        if q is not None and self.calculate_rung(m, n) > q:
            raise ValueError(f"{q} is not a valid rung for provided membership grades")

    def __str__(self):
        return f"<{self.m}, {self.n}, {self.q}>"

    def __add__(self, other):
        rung = int(max(self.q, other.q))

        other_m = self.to_decimal(other.m)
        m_sum = ((self._m ** rung) + (other_m ** rung) - ((self._m ** rung) * (other_m ** rung))) ** self.to_decimal(
            1 / rung)

        other_n = self.to_decimal(other.n)
        n_sum = self._n * other_n

        return QROFN(m_sum, n_sum)

    def __mul__(self, other):
        if isinstance(other, QROFN):
            rung = int(max(self._q, other.q))

            other_m = self.to_decimal(other.m)
            m_product = self._m * other_m

            other_n = self.to_decimal(other.n)
            n_product = (1 - (1 - self._n ** rung) * (1 - other_n ** rung)) ** self.to_decimal(1 / rung)

            product = QROFN(m_product, n_product)
        elif type(other) in [int, float, decimal.Decimal]:
            product = self.multiply_by_const(other)
        else:
            raise TypeError

        return product

    def multiply_by_const(self, c):
        if c <= 0:
            raise ValueError("Multiplication by non-positive scalar is not defined")

        if not isinstance(c, decimal.Decimal):
            c = self.to_decimal(c)

        m_product = (1 - (1 - self._m ** self._q) ** c) ** self.to_decimal(1 / self._q)
        n_product = self._n ** c
        product = QROFN(m_product, n_product)

        return product

    def __gt__(self, other):
        # Total ordering
        if self.score > other.score:
            return True
        if self.score == other.score:
            return self.accuracy > other.accuracy

        return False

    def __eq__(self, other):
        # Total ordering equality
        return self.score == other.score and self.accuracy == other.accuracy

    @classmethod
    def calculate_rung(cls, m, n):
        rung = 1
        power_sum = m + n
        while power_sum > 1:
            rung += 1
            power_sum = m ** rung + n ** rung
        return rung

    @classmethod
    def to_decimal(cls, number):
        return decimal.Decimal(str(number))

    def calculate_score(self):
        return self._m ** self._q + self._n ** self._q

    def calculate_accuracy(self):
        return self._m ** self._q - self._n ** self._q
