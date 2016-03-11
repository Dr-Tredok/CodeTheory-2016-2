from src.field import FqField
from src.polynomial import PolynomialZ2
from src.polynomial import Polynomial

# Example: F16 = Z2/<x^4 + x + 1>
#f = FqField(2, 4, '10011')
#f.list_elements()

# Example: F9 = Z3 / <x² + 2x + 2>
#g = FqField(3, 2, '122')
#g.list_elements()

a = Polynomial(3, [1, 0, 0, 0])
b = Polynomial(3, [1, 2, 0])
print(a.is_irreducible())
#print(PolynomialZ2('101').is_irreducible())

#h = FqField(3, 3, '1212')
