from src.polynomial import PolynomialZ2

a = PolynomialZ2('100001')
b = PolynomialZ2('101000')

print(a.coefficients, b.coefficients)

c = a.sum(b)
print(c.bin_representation, c.degree)

d = a.product(b)
print(d.bin_representation, d.degree)
