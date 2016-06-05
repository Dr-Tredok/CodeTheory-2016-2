class PolynomialZ2(object):
    """A Polynomial w/coefficients in Z2"""
    def __init__(self, coefficients = None, bytestring = True):
        """ Inicializa un polinomio en Z2[X] de grado a lo más 31. Default: 0 """
        super(PolynomialZ2, self).__init__()
        if coefficients is None:
            self.coefficients = 0
            self.degree = 0
        elif bytestring:
            self.from_bytestring(coefficients)
        else:
            self.coefficients = coefficients
            self.degree = coefficients.bit_length() - 1

    def from_bytestring(self, coefficients):
        """@param coefficients is a string '100101' equiv to x⁵ + x² + 1"""
        coefficients = coefficients.lstrip('0')
        lcoeff = len(coefficients)
        # Limitar a un entero
        if lcoeff > 32:
            raise NotImplementedError()
        self.coefficients = int(coefficients, 2)
        self.degree = lcoeff - 1

    def __eq__(self, other):
        if type(other) is int:
            return self.coefficients == other
        if type(other) == type(self):
            return self.coefficients == other.coefficients
        raise TypeError()

    def __ne__(self, other):
        return not self == other

    def is_zero(self):
        return self.coefficients == 0

    def clone(self):
        return PolynomialZ2(coefficients=self.coefficients, bytestring=False)

    # XOR
    def __add__(self, poly):
        return PolynomialZ2(coefficients=self.coefficients ^ poly.coefficients, bytestring=False)

    def __neg__(self):
        return self # in Z2 is the same

    # self * poly
    def __mul__(self, poly):
        r = 0
        a = self.coefficients
        b = poly.coefficients
        while a != 0: # product
            if (a & 1) != 0:
                r = r ^ b   # sum term
            b = b << 1 # xtimes
            a = a >> 1 # next term
        return PolynomialZ2(coefficients=r, bytestring=False)

    # self % poly
    def __mod__(self, poly):
        if poly.is_zero(): # division entre 0
            raise ZeroDivisionError()
        if self.is_zero(): # 0 / n = 0n + 0
            return PolynomialZ2()

        coefficients = poly.coefficients # xor later

        if poly.degree > self.degree: # quotient will be 0
            return self.clone()
        elif self.degree > poly.degree:
            coefficients = coefficients << (self.degree - poly.degree) # make degree be equal

        coefficients = self.coefficients ^ coefficients # difference
        return PolynomialZ2(coefficients=coefficients, bytestring=False) % poly

    # String representation
    def __str__(self):
        return bin(self.coefficients) # only bits

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.coefficients)

    def __int__(self):
        return self.coefficients

class Polynomial(object):
    """ Polinomio cuyos coeficientes son de otra clase, en particular de GF(q)"""
    def __init__(self, coefficients, field):
        """ coefficients - [T]
            [a, b, c, d] equiv ax³ + bx² + cx + d
            field - F<T> provee operaciones de suma y producto
        """
        super(Polynomial, self).__init__()
        if coefficients == []:
            self.coefficients = [field.zero()]
            self.degree = 0
        else:
            self.coefficients = coefficients
            self.degree = len(coefficients) - 1
        self.field = field

    def is_zero(self):
        return all([e.is_zero() for e in self.coefficients])

    def clone(self):
        return Polynomial(list(self.coefficients), self.field)

    def __add__(self, poly):
        degree = max(self.degree, poly.degree)
        coeff = []
        for i in range(1, degree + 2):
            if i > self.degree + 1:
                coeff = poly.coefficients[:-i+1] + coeff
                break
            if i > poly.degree + 1:
                coeff = self.coefficients[:-i+1] + coeff
                break
            coeff.insert(0, self.field.sum(self.coefficients[-i], poly.coefficients[-i]))

        fst = 0
        for i in range(degree + 1):
            if coeff[i] == 0:
                fst += 1
            else:
                break

        return Polynomial(coeff[fst:], self.field)

    def __sub__(self, poly):
        coefficients = [-a for a in poly.coefficients]
        return self + Polynomial(coefficients, self.field)

    def __neg__(self):
        coefficients = [-a for a in self.coefficients]
        return Polynomial(coefficients, self.field)

    def sproduct(self, element):
        coeff = [self.field.product(x, element) for x in self.coefficients]
        return Polynomial(coeff, self.field)

    def __mul__(self, poly):
        if self.is_zero() or poly.is_zero():
            return Polynomial.zero(self.field)

        degree = self.degree + poly.degree
        result = Polynomial.zero(self.field)
        a = self.degree
        b = poly.clone()

        while a >= 0:
            if self.coefficients[a] != 0:
                result = result + b.sproduct(self.coefficients[a])
            a -= 1
            b.coefficients += [self.field.zero()]

        return result

    def __divmod__(self, poly):
        if poly.is_zero():
            raise ZeroDivisionError()

        q = Polynomial.zero(self.field)
        r = self.clone()
        c = poly.coefficients[0]

        while r.degree >= poly.degree:
            coeff = [self.field.division(r.coefficients[0], c)] + [self.field.zero()]*(r.degree - poly.degree)
            s = Polynomial(coeff, self.field)
            q = q + s
            r = r - s*poly
            if r.is_zero():
                break

        return (q, r)

    def eval(self, alpha):
        """ Evalua un polinomio en alpha, raíz del campo """
        cf = [self.coefficients[-1]]
        x = alpha.clone() # elementos del campo deben ser clonables?
        for i in range(2, self.degree + 2): # empezar en termino x^1 hasta x^n
            if not self.coefficients[-i].is_zero():
                cf.append(self.field.product(x,self.coefficients[-i]))
            x = self.field.product(x, alpha) # elevar para la sig potencia
        c = self.field.zero()
        for v in cf:
            c = self.field.sum(c, v)
        return c

    @staticmethod
    def euclides(field, fx, gx, condition=lambda rk, r: rk.is_zero()):
        assert(not fx.is_zero())
        assert(not gx.is_zero())
        assert(gx.degree <= fx.degree)

        s0 = Polynomial([field.unity()], field)
        s1 = Polynomial.zero(field)
        t0 = Polynomial.zero(field)
        t1 = Polynomial([field.unity()], field)
        r0 = fx
        r1 = gx
        # rk = ak fx + bk gx
        while True:
            qk, rk = divmod(r0, r1)#r.__div_step(r0)
            assert(rk == r0 - qk * r1)
            sk = s0 - (qk * s1)
            tk = t0 - (qk * t1)
            assert(rk == fx * sk + gx * tk)
            if condition(rk, r0):
                break
            r0 = r1
            r1 = rk
            s0 = s1
            s1 = sk
            t0 = t1
            t1 = tk
        return (sk, tk, rk)

    @staticmethod
    def zero(field):
        return Polynomial([field.zero()], field)

    def __str__(self):
        return str(self.coefficients)#str([int(i) for i in self.coefficients])

    def __eq__(self, other):
        if type(other) != type(self):
            raise NotImplementedError()
        return self.degree == other.degree and all([self.coefficients[i] == other.coefficients[i] for i in range(self.degree + 1)])

    def __bytes__(self):
        return bytes([int(i) for i in self.coefficients])

    @staticmethod
    def from_bytes(b, field):
        coefficients = [field.element(b[i]) for i in range(len(b))] # cada entrada corresponde a un numero.. este se le pasa al campo y genera un elemento en él
        return Polynomial(coefficients, field)
