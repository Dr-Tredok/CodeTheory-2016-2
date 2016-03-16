import math
from .putils import *

# Returns a PolynomialZp
# Check if are numeric and apply % prime
# empty string is zero
def create_poly(prime, coefficients):
    if prime == 2:
        return PolynomialZ2(coefficients)
    elif prime > 2:
        return Polynomial(prime, list(map(lambda x: int(x), coefficients)))
    else:
        raise Exception("Not a valid prime!")


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

class Polynomial(PolynomialZp):
    """A polynomial w/coefficients in Zp, p > 2"""
    def __init__(self, prime, coefficients):
        super(Polynomial, self).__init__(prime)
        if coefficients == [] or coefficients == [0]:
            self.coefficients = [0]
            self.degree = 0
            return
        # [1, 2, 3] := x³ + 2x² + 3
        self.coefficients, self.degree = drop_zeros(coefficients)
        self.degree -= 1

    def sum(self, poly):
        """Return the sum self + poly over Zp[x]"""
        if self.prime != poly.prime:
            raise Exception("!= prime")

        return Polynomial(self.prime, sum_lists(self.coefficients, self.degree, poly.coefficients, poly.degree, self.prime))

    def scalar_product(self, n):
        return Polynomial(self.prime, scprod_list(self.coefficients, n, self.prime))

    def product(self, poly):
        """Return the product self * poly over Zp[x]"""
        if self.prime != poly.prime:
            raise Exception("!= prime")

        sindex = 1 # list entry
        sdegree = self.degree # how many zeroes will be?
        rindex = self.degree + poly.degree

        result = scprod_list(poly.coefficients, self.coefficients[0], self.prime) + [0]*sdegree

        for j in range(sdegree):
            sdegree -= 1
            result = sum_lists(scprod_list(poly.coefficients, self.coefficients[sindex], self.prime) + [0]*sdegree, poly.degree + sdegree, result, rindex, self.prime)
            sindex += 1

        return Polynomial(self.prime, result)

    def is_irreducible(self):
        """Return True if self is irreducible in Zp[x]"""
        # ¿f(x) irreducible, Zp?
        # u(x) = x
        ux = Polynomial(self.prime, [1, 0])
        mx = Polynomial(self.prime, [-1, 0])
        # i = 1 to floor(m/2)
        for i in range(math.floor(self.degree/2)):
        #   u(x) = u(x)^p mod f(x)
            upx = Polynomial(self.prime, list(ux.coefficients))
            for i in range(1, self.prime):
                ux = ux.product(upx)
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
        if self.coefficients == [0]:
            return Polynomial(self.prime, list(poly.coefficients))
        if poly.coefficients == [0]:
            return Polynomial(self.prime, list(self.coefficients))

        ax, bx = self, poly
        if self.degree <= poly.degree:
            bx, ax = self, poly
        rx = ax.remainder(bx)

        return bx.gcd(rx)

    def remainder(self, poly):
        """Return the remainder self % poly over Zp[x]"""
        if self.prime != poly.prime:
            raise Exception("!= prime")

        # poly != 0
        if poly.coefficients == [0]:
            raise Exception("not even here!")
        # always 0
        if self.coefficients == [0]:
            return Polynomial(self.prime, [0])

        # we're done
        if self.degree < poly.degree:
            return Polynomial(self.prime, list(self.coefficients))

        rx = list(poly.coefficients) # original
        if self.degree > poly.degree:
            rx += [0]*(self.degree - poly.degree) # eq to multiply
        rx = scprod_list(rx, -1, self.prime)
        rx = sum_lists(self.coefficients, self.degree, rx, len(rx)-1, self.prime)

        return Polynomial(self.prime, rx).remainder(poly)

    def __str__(self):
        s = ''
        degree = self.degree
        for i in range(self.degree + 1):
            if self.coefficients[i] != 0 and degree > 0:
                s += str(self.coefficients[i]) + 'x^' + str(degree) + ' + '
            if degree == 0:
                s += str(self.coefficients[i])
            degree -= 1
        return s

class PolynomialZ2(PolynomialZp):
    """A Polynomial w/coefficients in Z2"""

    SIZE = 8 # bits per element - test

    def __init__(self, coefficients = None):
        super(PolynomialZ2, self).__init__(2)
        if coefficients is None or coefficients == '0': # default is zero
            self.coefficients = [0]
            self.degree = 0
            self.__length = 1 # list length (different from degree since every entry is SIZE bits)
        else:
            self.coefficients = []
            self.__set_poly(coefficients)

    def __set_poly(self, coefficients):
        """@param coefficients is a string '100101' equiv to 1 + x² + x⁵"""
        coefficients = coefficients.lstrip('-0') # drop unused zero
        bits_length = len(coefficients)
        self.degree = bits_length - 1 # last entry different from zero

        s_bytes = math.ceil(bits_length / PolynomialZ2.SIZE) # elements in list
        self.__length = s_bytes # performance

        index = 0
        overflow = bits_length - (s_bytes - 1)*PolynomialZ2.SIZE
        # get int representation
        if overflow > 0:
            self.coefficients.append(int(coefficients[0:overflow], 2))
            index = overflow
            s_bytes -= 1
        for i in range(0, s_bytes):
            #print(index, index+PolynomialZ2.SIZE)
            self.coefficients.append(int(coefficients[index:PolynomialZ2.SIZE+index], 2)) # get SIZE byte group
            index += PolynomialZ2.SIZE # bytes loaded

    def __str_value(self):
        if self.coefficients == [0]:
            return '0'
        # bin
        br_str = ''
        for i in self.coefficients:
            s = bin(i).lstrip('-0b')
            l = len(s)
            if l < PolynomialZ2.SIZE:
                br_str += '0'*(PolynomialZ2.SIZE - l)
            br_str += s
        return br_str.lstrip('0')

    def __update_values(self):
        """ Will update a polynomial attributes based on its list of coefficients """
        # drop left zero
        self.coefficients, self.__length = drop_zeros(self.coefficients)

        if self.coefficients == [0]:
            self.degree = 0
            return

        # degree
        last_group = len(bin(self.coefficients[0]).lstrip('-0b')) - 1
        self.degree = PolynomialZ2.SIZE*(self.__length - 1) + last_group

    def __clone(self):
        p = PolynomialZ2()
        p.coefficients = list(self.coefficients)
        p.__length = self.__length
        p.degree = self.degree
        return p

    def sum(self, poly):
        p = PolynomialZ2() # polynomial init
        p.coefficients, p.__length = xor_lists(self.coefficients, self.__length-1, poly.coefficients, poly.__length-1)
        p.__update_values()

        return p

    def product(self, poly):
        # degree of poly tell us xtimes
        degree = self.degree
        p = PolynomialZ2()

        for c in self.__str_value():
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

        return p

    def is_irreducible(self):
        """Return True if self is irreducible in Z2[x]"""
        # ¿f(x) irreducible, Zp?
        # u(x) = x
        ux = PolynomialZ2('10')
        mx = PolynomialZ2('-10')
        # i = 1 to floor(m/2)
        for i in range(math.floor(self.degree/2)):
        #   u(x) = u(x)^p mod f(x)
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
        #print("str()", self.degree)
        for c in self.__str_value():
            if c == '1' and degree > 0:
                string += 'x^' + str(degree) + ' + '
            if degree == 0:
                string += c
            degree -= 1
        return string
