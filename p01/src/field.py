from .polynomial import PolynomialZp
from .polynomial import create_poly

class FqField(object):
    """Field Fq = Zp/<f(x)> w/deg(f) = n"""
    def __init__(self, prime, exponent, poly):
        super(FqField, self).__init__()
        # lel
        self.prime = prime
        self.length = pow(prime, exponent) # = q

        if exponent == 1:
            self.elements = [create_poly(prime, str(i)) for i in range(prime)]
            return

        self.gpolynomial = create_poly(self.prime, poly)
        alpha = create_poly(self.prime, '1 0')
        self.elements = [create_poly(self.prime, '0'), create_poly(self.prime, '1'), alpha]

        if self.gpolynomial.degree != exponent:
            raise Exception("Nope. Nope. Nope. Must: deg(fx) = n")

        if not self.gpolynomial.is_irreducible():
            raise Exception("Reducible polynomial")

        # generate field
        for i in range(self.length - 3):
            # alpha^n = alpha * alpha^(n-1) % f(x)
            n = self.elements[-1].product(alpha).remainder(self.gpolynomial)
            self.elements.append(n)
            if n.is_neutral():
                raise Exception("Ooops.. neutral before");

    def list_elements(self):
        return list(self.elements)

    def get_isum(self, poly):
        return self.elements[self.elements.index(poly.scalar_product(-1))]

    # alpha^i * alpha^(q - 1 - i) = alpha^(q - 1 mod q-1) = alpha^0 = 1
    def get_iproduct(self, poly):
        index = self.length - 1 # q - 1
        index -= self.elements.index(poly) - 1 # q - 1 - i
        return self.elements[(index % (self.length - 1)) + 1] # starts w/0

    def get_apower(self, poly):
        return self.elements.index(poly) - 1 # duh

    def sum(self, poly1, poly2):
        return poly1.sum(poly2).remainder(self.gpolynomial)

    def product(self, poly1, poly2):
        return poly1.product(poly2).remainder(self.gpolynomial)

    # creates a polynomial inside Fq
    def reduce(self, string):
        poly = create_poly(self.prime, string) # safe function
        return poly.remainder(self.gpolynomial) # get element in field

    # given an alpha return isum, iproduct
    def inv_alpha(self, n):
        if n > self.length - 2 or n < 0:
            raise Exception("Not a valid alpha")
        ia = self.get_isum(self.elements[n + 1])
        index = self.length - 1 - n
        im = self.elements[(index % (self.length - 1)) + 1]
        return ia, im
