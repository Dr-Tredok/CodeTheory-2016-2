import math

class Polynomial(object):
    """A polynomial w/coefficients in Zp"""
    def __init__(self, prime, coefficients = []):
        super(Polynomial, self).__init__()
        self.prime = prime
        # [1, 2, 3] := x³ + 2x² + 3
        self.coefficients = coefficients
        self.degree = len(coefficients) - 1

    def sum(self, poly):
        """Return the sum self + poly over Zp[x]"""
        if self.prime != poly.prime:
            raise Exception("!= prime")

        return Polynomial(self.prime, sum_coefficients_list(self.coefficients, self.degree, poly.coefficients, poly.degree, self.prime))


    def product(self, poly):
        """Return the product self * poly over Zp[x]"""
        if self.prime != poly.prime:
            raise Exception("!= prime")

        sindex = 1 # list entry
        sdegree = self.degree # how many zeroes will be?
        rindex = self.degree + poly.degree

        result = [(self.coefficients[0]*y)%self.prime for y in poly.coefficients] + [0]*sdegree

        for j in range(sdegree):
            sdegree -= 1
            result = sum_coefficients_list([self.coefficients[sindex]*y for y in poly.coefficients] + [0]*sdegree, poly.degree + sdegree, result, rindex, self.prime)
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
            dx = self.gcd(Polynomial(self.prime, sum_coefficients_list(ux.coefficients, ux.degree, mx.coefficients, 1, self.prime)))
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
        rx = [(-1)*x for x in rx] # substraction
        rx = sum_coefficients_list(self.coefficients, self.degree, rx, len(rx)-1, self.prime)

        # drop 0 not used
        dindex = 0
        for j in rx:
            if j == 0:
                dindex += 1
            else:
                break
        if dindex == len(rx):
            dindex = -1 # all were 0.. so we get the last

        return Polynomial(self.prime, rx[dindex:]).remainder(poly)

    def __eq__(self, other):
        if type(self) is type(other):
            return [x % prime for x in self.coefficients] == [x % prime for x in other.coefficients] and self.prime == other.prime
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

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


def sum_coefficients_list(slist, sindex, plist, pindex, prime):
    rindex = max(sindex, pindex)

    result = [0] * (rindex + 1)

    while sindex >= 0 and pindex >= 0:
        result[rindex] = (slist[sindex] + plist[pindex]) % prime
        rindex -= 1
        pindex -= 1
        sindex -= 1

    if sindex > pindex:
        while sindex >= 0:
            result[sindex] = slist[sindex]
            sindex -= 1
    elif pindex > sindex:
        while pindex >= 0:
            result[pindex] = plist[pindex]
            pindex -= 1

    return result

class PolynomialZ2(object):
    """A Polynomial w/coefficients in Z2"""
    def __init__(self, coefficients = None):
        super(PolynomialZ2, self).__init__()
        if coefficients is None:
            self.coefficients = 0
            self.bin_representation = '0'
            self.degree = 0
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
        self.degree = len(self.bin_representation) - 1

    def __update_values(self):
        self.bin_representation = bin(self.coefficients).lstrip('-0b')
        self.degree = len(self.bin_representation) - 1

    # XOR
    def sum(self, poly):
        p = PolynomialZ2()
        p.coefficients = self.coefficients ^ poly.coefficients
        p.__update_values()
        return p

    def product(self, poly):
        # degree of poly
        degree = self.degree

        p = PolynomialZ2()

        # product of every term
        for c in self.bin_representation:
            if c == '1':
                p.coefficients = p.coefficients ^ (poly.coefficients << degree)
            degree -= 1
        p.__update_values()
        return p

    # self % poly
    def remainder(self, poly):
        # get degree of both
        degree_poly = poly.degree
        degree = self.degree

        p = PolynomialZ2()
        coefficients = poly.coefficients # xor later

        if degree_poly > degree: # quotient will be 0
            p.coefficients = self.coefficients
            p.bin_representation = self.bin_representation
            p.degree = self.degree
            return p
        elif degree > degree_poly:
            coefficients = coefficients << (degree - degree_poly) # make degree be equal

        p.coefficients = self.coefficients ^ coefficients
        p.__update_values()
        return p

    def is_irreducible(self):
        """Return True if self is irreducible in Zp[x]"""
        # ¿f(x) irreducible, Zp?
        # u(x) = x
        ux = PolynomialZ2('10')
        mx = PolynomialZ2('10')
        # i = 1 to floor(m/2)
        for i in range(math.floor(self.degree/2)):
        #   u(x) = u(x)^p mod f(x)
            ux = ux.product(ux)
            ux = ux.remainder(self)
        #   d(x) = mcd(f(x), u(x) - x)
            dx = self.gcd(ux.sum(mx))
        #   d(x) != 1 -> Reducible
            if dx.coefficients != 1:
                return False
        # end
        # -> irreducible
        return True

    def gcd(self, poly):
        if self.coefficients == 0:
            return PolynomialZ2(poly.bin_representation)
        if poly.coefficients == 0:
            return PolynomialZ2(self.bin_representation)

        ax, bx = self, poly
        if self.degree <= poly.degree:
            bx, ax = self, poly
        rx = ax.remainder(bx)

        return bx.gcd(rx)

    # String representation
    def __str__(self):
        degree = self.degree
        string = ''
        for c in self.bin_representation:
            if c == '1' and degree > 0:
                string += 'x^' + str(degree) + ' + '
            if degree == 0:
                string += c
            degree -= 1
        return string
