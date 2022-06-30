import decimal
from abc import abstractmethod


class FuzzyNumber(object):
    _m: decimal.Decimal = None
    _n: decimal.Decimal = None
    _q: int

    def __init__(self, *args, **kwargs):
        pass

    @property
    def m(self):
        return self._m

    @property
    def n(self):
        return self._m

    @property
    def q(self):
        return self._m

    @abstractmethod
    def multiply_by_const(self, c):
        pass
