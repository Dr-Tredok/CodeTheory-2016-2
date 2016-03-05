import math

class Polynomial(object):
    """A polynomial w/coefficients in Zp"""
    def __init__(self, prime, coefficients = []):
        super(Polynomial, self).__init__()
        self.prime = prime
        # [1, 2, 3] := x³ + 2x² + 3
        self.coefficients = coefficients

    def sum(self, poly):
        """Return the sum self + poly over Zp[x]"""
        if self.prime != poly.prime:
            raise Exception("!= prime")
        # Suma self.coefficients[i] + poly.coefficients[i] % prime
        pass

    def product(self, poly):
        """Return the product self * poly over Zp[x]"""
        # Similar a sum
        pass

    def is_irreducible(self):
        """Return True if self is irreducible in Zp[x]"""
        # ¿f(x) irreducible, Zp?
        # u(x) = x
        # i = 1 to floor(m/2)
        #   u(x) = u(x)^p mod f(x)
        #   d(x) = mcd(f(x), u(x) - x)
        #   d(x) != 1 -> Reducible
        # end
        # -> irreducible
        pass

    def remainder(self, poly):
        """Return the remainder self % poly over Zp[x]"""
        pass

    def __eq__(self, other):
        if type(self) is type(other):
            return [x % prime for x in self.coefficients] == [x % prime for x in other.coefficients] and self.prime == other.prime
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def degree(self):
        return len(self.coefficients) - 1

class PolynomialZ2(Polynomial):
    """A Polynomial w/coefficients in Z2"""
    def __init__(self, coefficients = None):
        super(PolynomialZ2, self).__init__(2)
        if coefficients is None:
            self.coefficients = 0
            self.bin_representation = '' # is set when coefficients_vector is called
        else:
            self.set_poly(coefficients)

    def set_poly(self, coefficients):
        """@param coefficients is a string '100101' equiv to 1 + x² + x⁵"""
        # 32 bits per element
        s_bytes = math.ceil(len(coefficients) / 32)
        # :B
        if s_bytes > 1:
            raise NotImplementedError('Ups..')
        # get int representation
        self.coefficients = int(coefficients, 2)
        self.bin_representation = coefficients

    def degree(self):
        return len(self.coefficients_vector()) - 1

    # XOR
    def sum(self, poly):
        p = PolynomialZ2()
        p.coefficients = self.coefficients ^ poly.coefficients

        return p

    def product(self, poly):
        # degree of poly
        degree = self.degree()

        p = PolynomialZ2()

        # product of every term
        for c in self.bin_representation:
            if c == '1':
                p.coefficients = p.coefficients ^ (poly.coefficients << degree)
            degree -= 1

        return p

    # self % poly
    def remainder(self, poly):
        # get degree of both
        degree_poly = self.degree()
        degree = self.degree()

        p = PolynomialZ2()
        coefficients = poly.coefficients # xor later

        if degree_poly > degree: # quotient will be 0
            p.coefficients = self.coefficients
            p.bin_representation = self.coefficients_vector()
            return p
        elif degree > degree_poly:
            coefficients = coefficients << (degree - degree_poly) # make degree be equal

        p.coefficients = self.coefficients ^ coefficients

        return p

    # Safe poly.coefficients_vector
    # Unsafe poly.bin_representation
    def coefficients_vector(self):
        if self.bin_representation == '':
            self.bin_representation = bin(self.coefficients).lstrip('-0b')
        return self.bin_representation

    # String representation
    def __str__(self):
        degree = len(self.coefficients_vector()) - 1
        string = ''
        for c in self.coefficients_vector():
            if c == '1' and degree > 0:
                string += 'x^' + str(degree) + ' + '
            if degree == 0:
                string += c
            degree -= 1
        return string
