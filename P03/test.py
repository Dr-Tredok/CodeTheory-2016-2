from polynomial import *
from field import *
from rs import *

class dummyField(object):
    """docstring for dummyField"""
    def __init__(self):
        super(dummyField, self).__init__()

    def zero(self):
        return 0

    def sum(self, a, b):
        return (a + b) % 2

    def product(self, a, b):
        return (a * b) % 2

    def division(self, a, b):
        if a == 0 and b == 1:
            return 0
        elif a == 1 and b == 1:
            return 1
        raise ZeroDivisionError()

f = GF.roman()
rs = RS(15, 11, 5, f)
print(f.pow)
rx = Polynomial([f.unity()] +  [f.zero()]*3 + [f.unity()]*3 + [f.zero()]*5 + [f.unity()], f)
print(rs.decode(rx))
