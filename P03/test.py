from polynomial import *
from field import *

class dummyField(object):
    """docstring for dummyField"""
    def __init__(self):
        super(dummyField, self).__init__()

    def zero(self):
        return 0

    def sum(self, a, b):
        return a + b

    def product(self, a, b):
        return a * b

    def division(self, a, b):
        return a/b

f = dummyField()
a = Polynomial([1, 0, 0, 1, 1], f)
b = Polynomial([1, 1], f)

gf = GF.qr()
print(gf.pow)
c = Polynomial([gf[0], gf[1], gf[0]], gf)
d = Polynomial([gf[2]], gf)
print("a", c)
print("b", d)
q, r = divmod(c, d)
assert(r.is_zero())
