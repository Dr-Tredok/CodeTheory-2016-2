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

    SIZE = 2 # bits per element

    def __init__(self, coefficients = None):
        super(PolynomialZ2, self).__init__(2)
        if coefficients is None: # default is zero
            self.coefficients = [0]
            self.degree = 0
            self.bin_representation = '0'
            self.__length = 1
        else:
            self.coefficients = []
            self.set_poly(coefficients)

    def set_poly(self, coefficients):
        """@param coefficients is a string '100101' equiv to 1 + x² + x⁵"""

        coefficients = coefficients.lstrip('0') # drop unused zero
        self.degree = len(coefficients) - 1 # last known zero

        s_bytes = math.ceil(len(coefficients) / PolynomialZ2.SIZE) # elements in list
        index = 0

        # get int representation
        for i in range(1, s_bytes):
            self.coefficients.append(int(coefficients[index:PolynomialZ2.SIZE*i], 2)) # get 32 byte group
            index = i*PolynomialZ2.SIZE # bytes loaded

        self.coefficients.append(int(coefficients[index:], 2)) # less significative ones
        self.bin_representation = coefficients # duh
        self.__length = s_bytes # performance

    def __update_values(self):
        """ Will update a polynomial attributes based on its list of coefficients """
        # drop left zero
        left_zero = True
        i = 0

        while left_zero and i < self.__length:
            if self.coefficients[i] == 0:
                i += 1
            else:
                left_zero = False

        # was zero
        if i == self.__length:
            self.coefficients = [0]
            self.degree = 0
            self.bin_representation = '0'
            self.__length = 1
            return

        self.coefficients = self.coefficients[i:]
        self.__length = self.__length - i

        # degree
        last_group = len(bin(self.coefficients[0]).lstrip('-0b')) - 1
        self.degree = PolynomialZ2.SIZE*(self.__length - 1) + last_group

        # bin
        br_str = ''
        for i in self.coefficients:
            s = bin(i).lstrip('-0b')
            l = len(s)
            if l < PolynomialZ2.SIZE:
                br_str += '0'*(PolynomialZ2.SIZE - l)
            br_str += s
        self.bin_representation = br_str.lstrip('0')

    def sum(self, poly):
        p = PolynomialZ2() # polynomial init
        p.coefficients, p.__length = xor(self.coefficients, self.__length, poly.coefficients, poly.__length)
        p.__update_values()

        return p

    def product(self, poly):
        # degree of poly tell us xtimes
        degree = self.degree

        p = PolynomialZ2()
        # so....

        return p

    """
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

    """

""" Bitwise methods for arrays """
def xor(array, length, sarray, slength):
    """ Will xor self.coefficients with @param array list with @param length elements """
    index_self = slength - 1
    index_poly = length - 1

    # result
    length = max([slength, length])
    index_p = length - 1
    coeff = [0]*length

    while index_poly >= 0 and index_self >= 0:
        coeff[index_p] = array[index_poly] ^ sarray[index_self]
        index_poly -= 1
        index_self -= 1
        index_p -= 1

    if index_poly > index_self:
        while index_poly >= 0:
            coeff[index_poly] = array[index_poly]
            index_poly -= 1
    elif index_self > index_poly:
        while index_self >= 0:
            coeff[index_self] = sarray[index_self]
            index_self -= 1

    return coeff, length

#
#   Panic.
#
def left_shift(array, length):
    coeff = [0] * length # result

    overflow = 0
    i = length - 1

    while i >= 0:
        coeff[i] = (array[i] << 1) ^ overflow
        overflow = (array[i] >> PolynomialZ2.SIZE) & 1
        i -= 1

    return coeff
