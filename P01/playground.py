from src.field import FqField
from src.polynomial import create_poly, PolynomialZ2, Polynomial

g = FqField(3, 2, '122')
g.list_elements()

a = PolynomialZ2('111')
b = PolynomialZ2('11')
print(a.product(b))
