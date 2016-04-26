# Este archivo tuvo el propósito de hacer la prueba y error del programa, a pesar de que existe "playground", ese otro tiene unstrucciónes y ejemplos.
# este es un maldito desmadre.

from src.field import FqField
from src.polynomial import create_poly
from src.polynomial import PolynomialZp

# Example: F16 = Z2/<x^4 + x + 1>
#f = FqField(2, 4, '10011')
#f.list_elements()

# Example: F9 = Z3 / <x² + 2x + 2>
g = FqField(3, 2, '122')
g.list_elements()

print(g.get_iproduct(g.elements[3]))
