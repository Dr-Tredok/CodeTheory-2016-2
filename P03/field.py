from polynomial import PolynomialZ2

class GF(object):
    """ Field Fq = Z2/<f(x)> w/deg(f) <= 31"""
    def __init__(self, exponent, poly, root):
        super(GF, self).__init__()
        self.gpolynomial = PolynomialZ2(poly)
        self.alpha = PolynomialZ2(root)
        self.len = pow(2, exponent)

        if self.gpolynomial.degree != exponent or self.alpha.degree >= self.gpolynomial.degree:
            raise ValueError()

        # generar el campo: solo el grupo multiplicativo
        self.elements = [PolynomialZ2('1'), self.alpha]
        self.pow = {self.elements[0]: 0, self.alpha: 1} # guardar las potencias asociadas
        for i in range(2, self.len - 1):
            n = (self.elements[-1] * self.alpha) % self.gpolynomial
            self.elements.append(n) # agregar elemento
            self.pow[n] = i # potencia de la raíz
        assert((self.elements[-1] * self.alpha) % self.gpolynomial == self.elements[0])

    def each(self):
        for i in self.elements:
            yield i

    def sum(self, poly1, poly2):
        return (poly1 + poly2) % self.gpolynomial

    def gproduct(self, poly1, poly2): # producto de dos polinomios cualquiera
        return (poly1 * poly2) % self.gpolynomial

    def product(self, poly1, poly2): # producto de dos polinomios del campo
        if poly1.is_zero():
            return self.zero()
        if poly2.is_zero():
            return self.zero()

        i = self.pow[poly1]
        j = self.pow[poly2] # suma de potencias...
        return self.elements[(i + j) % (self.len - 1)]

    def inverse(self, poly):
        i = self.pow[poly]
        return self.elements[-i % (self.len - 1)] # inverso de un elemento del campo

    # creates a polynomial inside Fq
    def reduce(self, i):
        p = PolynomialZ2(i, bytestring=False) # crear polinomio
        if p.degree >= self.gpolynomial.degree: # si es de grado mayor, reducirlo al módulo
            p = p % self.gpolynomial
        return p

    def element(self, i):
        """ Devuelve el polinomio asociado a un entero """
        p = PolynomialZ2(i, bytestring=False)
        if p.degree >= self.gpolynomial.degree:
            raise ValueError() # debe ser un polinomio de grado menor
        return p

    def zero(self):
        return PolynomialZ2()

    def unity(self):
        return self.elements[0]

    def division(self, poly1, poly2): # divide dos elementos del campo
        i = self.pow[poly1]
        j = self.pow[poly2]
        return self.elements[(i - j) % (self.len - 1)] # diferencia de potencias

    def oproduct(self, poly, i): # producto por un escalar: la suma i veces de poly
        if i == 0:
            return self.zero()

        prod = poly
        for j in range(i - 1):
            prod = prod + poly
        return prod % self.gpolynomial

    def __len__(self):
        return self.len

    def __getitem__(self, key):
        return self.elements[key]

    @staticmethod
    def aes():
        return GF(8, '100011011', '11') # Generado por el polinomio usado en AES

    @staticmethod
    def primitive():
        return GF(8, '100011101', '10') # Generado por polinomio primitivo

    @staticmethod
    def qr():
        return GF(2, '111', '10')

    @staticmethod
    def roman():
        return GF(4, '10011', '10')
