from src.field import FqField
from src.polynomial import create_poly, PolynomialZ2, Polynomial

"""
    Aqui es donde hacemos pruebas. (Si no fuera por pereza e hicieramos pruebas unitarias).
    La forma correcta de crear un polinomio es a través de
        create_poly
            @param prime El número primo para Zp[x]
            @param coefficients Una cadena con los coeficientes del polinomio, separados por espacio y empezando por el grado mayor:
                e.g. x² +  x  = 1 0
                     x⁵ + 3x³ + 1 = 1 0 3 0 0 1
    Si se prefiere pueden usar PolynomialZ2 para polinomios en Z2. Se construyen a partir de una cadena representando el polinomio _sin_ espacio y en _binario_:
            PolynomialZ2('1011') = x³ + x + 1
    la clase Polynomial abarca polinomios en Z3 para arriba. Se construyen a partir de un arreglo con los coeficientes:
            Polynomial(3, [1, 2, 1, 0]) = x³ + 2x² + x en Z3[x]
    NOTA: Ambas clases esperan coeficientes en su respectivo campo... números entre 0..p. Para jugar existe create_poly.

    La clase Polynomial define todas las acciones posibles a realizar con dos polinomios. La clase FqField crea el campo:
        FqField
            @param prime El número primo para los coeficientes
            @param exponent El grado del polinomio, el exponente de prime, ya sabes..
            @param polynomial El polinomio con el que se desea generar el campo. Se espera en el mismo formato que create_poly

    Es todo lo que necesitas saber.

    Si explota el programa... bueno, es Python.
    Seguramente en mis pruebas ociosas no entré a esa parte de código que explota.. he seguido encontrando casos graciosos que no contemplo.
"""

#g = FqField(3, 2, '1 2 2')
#g.list_elements()

# a = PolynomialZ2('111')
# b = PolynomialZ2('11')
#print(a.product(b))

#h = FqField(2, 4, '1 1 0 0 1')
#h.list_elements()

#r = create_poly(3, '1 1 1')
#s = create_poly(3, '1 0 0 0 0 0')
#print(r.product(s))
