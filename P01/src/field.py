from polynomial import PolynomialZ2
from polynomial import Polynomial

class FqField(object):
    """Field Fq = Zp/<f(x)> w/deg(f) = n"""
    def __init__(self, prime, exponent, poly):
        super(FqField, self).__init__()
        # lel
        self.prime = prime
        self.exponent = exponent
        self.length = pow(prime, exponent) # = q

        # initialization
        if prime == 2:
            self.gpolynomial = PolynomialZ2(poly) # f(x)
            alpha = PolynomialZ2('10') # root
            self.elements = [PolynomialZ2('0'), PolynomialZ2('1'), alpha]
        else: # under construction...
            self.gpolynomial = Polynomial(prime)
            alpha = Polynomial(prime)
            self.elements = []

        # generate field
        for i in range(self.length - 3): #alpha^2 ... alpha^(q-2)
            # alpha^n = alpha * alpha^(n-1) % f(x)
            n = self.elements[-1].product(alpha).remainder(self.gpolynomial)
            self.elements.append(n) # index will be the power (-1)

    def list_elements(self):
        for i in self.elements:
            print(i)

    def get_isum(self, poly):
        pass

    # alpha^i * alpha^(q - 1 - i) = alpha^(q - 1 mod q-1) = alpha^0 = 1
    def get_iproduct(self, poly):
        index = self.length - 1
        index -= self.elements.index(poly) - 1
        return self.elements[(index % (self.length - 1)) + 1] # starts w/0

    def get_apower(self, poly):
        return self.elements.index(poly) - 1

    def sum(self, poly1, poly2):
        return poly1.sum(poly2)

    def product(self, poly1, poly2):
        return poly1.product(poly2)

# Example: F16 = Z2/<x^4 + x + 1>
f = FqField(2, 4, '10011')
f.list_elements()
