import math
from .putils import *

""" Abstract Class """
class PolynomialZp(object):
    def __init__(self, prime):
        """ Prime and string coefficients"""
        self.prime = prime;
        self.coefficients = None;

    def product(self, poly):
        pass

    def sum(self, poly):
        pass

    def is_irreducible(self):
        pass

    def remainder(self, poly):
        pass

    def gcd(self, poly):
        pass

    def is_neutral(self):
        return self.coefficients == [1]

    def scalar_product(self, n):
        pass

    def __eq__(self, other):
        if type(self) is type(other):
            return [x % self.prime for x in self.coefficients] == [x % self.prime for x in other.coefficients] and self.prime == other.prime
        return False

    def __ne__(self, other):
            return not self.__eq__(other)

    def __str__(self):
        return "Im a Polynomial"

class PolynomialZ2(PolynomialZp):
    """A Polynomial w/coefficients in Z2"""

    SIZE = 8 # bits per element - test for ascii

    def __init__(self, coefficients = None):
        super(PolynomialZ2, self).__init__(2)
        if coefficients is None: # default is zero
            self.coefficients = [0]
            self.degree = 0
            self.__length = 1 # list length (different from degree since every entry is SIZE bits)
        else:
            self.coefficients = []
            self.__set_poly(coefficients)

    def __set_poly(self, coefficients):
        """@param coefficients is a string '100101' equiv to 1 + x² + x⁵"""
        coefficients = drop_str_zeros(coefficients) # drop unused zero
        bits_length = len(coefficients)
        self.degree = bits_length - 1 # starts with degree zero

        s_bytes = math.ceil(bits_length / PolynomialZ2.SIZE) # elements in list
        self.__length = s_bytes # performance

        index = 0
        overflow = bits_length - (s_bytes - 1)*PolynomialZ2.SIZE # bits not in a SIZE group
        # get int representation
        if overflow > 0:
            self.coefficients.append(int(coefficients[0:overflow], 2))
            index = overflow
            s_bytes -= 1
        for i in range(0, s_bytes):
            self.coefficients.append(int(coefficients[index:PolynomialZ2.SIZE+index], 2)) # get SIZE byte group
            index += PolynomialZ2.SIZE # bytes loaded

    def str_value(self):
        if self.coefficients == [0]:
            return '0'
        # bin
        br_str = ''
        for i in self.coefficients:
            s = drop_str_zeros(bin(i))
            l = len(s)
            if l < PolynomialZ2.SIZE:
                br_str += '0'*(PolynomialZ2.SIZE - l)
            br_str += s
        return br_str.lstrip('0')

    def __update_values(self):
        """ Will update a polynomial attributes based on its list of coefficients """
        # drop left zero
        self.coefficients, self.__length = drop_zeros(self.coefficients)
        # degree
        last_group = len(drop_str_zeros(bin(self.coefficients[0]))) - 1
        self.degree = PolynomialZ2.SIZE*(self.__length - 1) + last_group

    def __clone(self):
        p = PolynomialZ2()
        p.coefficients = list(self.coefficients)
        p.__length = self.__length
        p.degree = self.degree
        return p

    def sum(self, poly):
        if self.prime != poly.prime:
            raise Exception("!= prime")

        p = PolynomialZ2() # polynomial init
        p.coefficients, p.__length = xor_lists(self.coefficients, self.__length-1, poly.coefficients, poly.__length-1)
        p.__update_values()

        return p

    def product(self, poly):
        if self.prime != poly.prime:
            raise Exception("!= prime")

        # degree of poly tell us xtimes
        degree = self.degree
        p = PolynomialZ2()

        for c in self.str_value(): # ñera
            if c == '1':
                shift = list(poly.coefficients)
                length = poly.__length
                for j in range(degree):
                    shift, length = left_shift_list(shift, length, PolynomialZ2.SIZE)   # << degree
                p.coefficients, p.__length = xor_lists(p.coefficients, p.__length - 1, shift, length - 1) # ^ result
            degree -= 1
        p.__update_values()

        return p

    def scalar_product(self, n):
        if n%2 == 1:
            return self.__clone()
        else:
            return PolynomialZ2()

    def remainder(self, poly):
        if self.prime != poly.prime:
            raise Exception("!= prime")

        # get degree of both
        degree_poly = poly.degree
        degree = self.degree

        # poly != 0
        if poly.coefficients == [0]:
            raise Exception("not even here!")
        # always 0
        if self.coefficients == [0]:
            return PolynomialZ2()

        p = poly.__clone()

        if degree_poly > degree: # quotient will be 0
            return self.__clone()
        elif degree > degree_poly:
            for j in range(degree - degree_poly):
                p.coefficients, p.__length = left_shift_list(p.coefficients, p.__length, PolynomialZ2.SIZE) # make degree be equal

        p.coefficients, p.__length = xor_lists(self.coefficients, self.__length - 1, p.coefficients, p.__length - 1)
        p.__update_values()

        return p.remainder(poly)

    def is_irreducible(self):
        """Return True if self is irreducible in Z2[x]"""
        # ¿f(x) irreducible, Zp?
        # u(x) = x
        ux = PolynomialZ2('10')
        mx = PolynomialZ2('-10')
        # i = 1 to floor(m/2)
        for i in range(math.floor(self.degree/2)):
        #   u(x) = u(x)^2 mod f(x)
            ux = ux.product(ux)
            ux = ux.remainder(self)
        #   d(x) = mcd(f(x), u(x) - x)
            dx = self.gcd(ux.sum(mx))
        #   d(x) != 1 -> Reducible
            if dx.coefficients != [1]:
                return False
        # end
        # -> irreducible
        return True

    def gcd(self, poly):
        if self.prime != poly.prime:
            raise Exception("!= prime")

        if self.coefficients == [0]:
            return poly.__clone()
        if poly.coefficients == [0]:
            return self.__clone()

        ax, bx = self, poly
        if self.degree <= poly.degree:
            bx, ax = self, poly

        rx = ax.remainder(bx)

        return bx.gcd(rx)

    # String representation
    def __str__(self):
        degree = self.degree
        string = ''

        for c in self.str_value():
            if c == '1' and degree > 0:
                string += 'x^' + str(degree) + ' + '
            if degree == 0:
                string += c
            degree -= 1
        return string

    def __eq__(self, other):
        if type(self) is type(other):
            return self.coefficients == other.coefficients and self.prime == other.prime
        return False

    def __hash__(self):
        # temporary fix since polynomials have at most 8 bits
        return self.coefficients[0]
