from polynomial import Polynomial as P
from field import GF

class RS(object):
    """docstring for RS"""
    def __init__(self, n, k, d, field):
        super(RS, self).__init__()
        # Parametros del código
        self.n = n
        self.k = k
        self.d = d
        assert(self.d == self.n - self.k + 1) # cota de singleton - RS es MDS
        # Campo
        self.field = field
        # Information set = {1, 2, ..., 2t}
        gx = P([field.unity(), -field.alpha], field) # x - a
        for i in range(2, d):
            gx = gx * P([field.unity(), -field[i]], field) # g * (x - a^i)
        self.gx = gx # polinomio generador
        assert(self.gx.degree == self.d - 1)
        q, r = divmod(P([field.unity()] + [field.zero()]*(self.n - 1) + [-field.unity()], field), self.gx)
        assert(r.is_zero()) # BCH view
        self.nk = P([field.unity()] + [field.zero()]*self.gx.degree, field) #x^2t
        assert(self.nk.degree == self.d - 1)
        self.t = int((self.d - 1) / 2) # capacidad de correción

    def encode_bytes(self, msg):
        assert(len(msg) <= self.k)
        poly = P.from_bytes(msg, self.field) # cargar polinomio asociado
        return self.encode(poly)

    def encode(self, poly):
        assert(poly.degree < self.k)
        sx = poly * self.nk # hacer espacio para entradas de verificación
        assert(sx.degree < self.n)
        qx, rx = divmod(sx, self.gx) # obtener residuo
        assert(rx.degree < self.gx.degree)
        assert(sx == self.gx * qx + rx)
        cx = sx - rx # palabra codificada
        self.pad_zeros(cx) # agregar ceros para evitar problemas...
        return cx

    def decode_bytes(self, cword):
        assert(len(cword) <= self.n)
        poly = P.from_bytes(cword, self.field) # cargar bloque
        return self.decode(poly)

    def pad_zeros(self, poly):
        # Crea el bloque de 255.. si se codifica en menos, al leer se agarran bloques de otro mensaje
        i = self.n - poly.degree - 1
        poly.coefficients = [self.field.zero()]*i + poly.coefficients

    def trim_zeros(self, poly):
        fst = 0 # eliminar ceros anteriores
        for i in range(len(poly.coefficients)):
            if poly.coefficients[i] == 0:
                fst += 1
            else:
                break
        return P(poly.coefficients[fst:], self.field)

    def decode(self, poly):
        poly = self.trim_zeros(poly) # cargar polinomio real
        assert(poly.degree < self.n)

        sx = []
        for i in range(1, self.nk.degree + 1): # calcular sindromes
            sx.insert(0, poly.eval(self.field[i])) # evaluar en a^i, i = 1..2t
        if all([si.is_zero() for si in sx]): # todos los sindromes son cero
            coeff = poly.coefficients[:-self.nk.degree] # mensaje en los k coeficientes de x^n-1 .. x^n-k
            decode =  P(coeff, self.field) # polinomio asociado
            assert(decode.degree < self.k)
            return decode

        fx = self.nk # x^2t
        gx = P(sx, self.field) # S(x) = s1 + s2 x + .. + s2t x^2t-1
        ak, bk, rk = P.euclides(self.field, fx, gx, lambda rk, r0: rk.degree < self.t and r0.degree >= self.t)
        assert(rk.degree < self.t)
        assert(bk.degree <= self.t)
        assert(rk == ak * fx + bk * gx) # from euclides
        b0 = bk.eval(self.field.zero())
        ib0 = self.field.inverse(b0)
        assert(self.field.product(b0, ib0) == self.field.unity())
        sigma = bk.sproduct(ib0) # bk(0)^-1 bk
        omega = rk.sproduct(ib0) # bk(0)^-1 rk
        assert(sigma.degree <= self.t) # capacidad de corrección
        assert(omega.degree < self.t)

        # ver raices...
        roots = [] # tendrá las posiciones de los errores
        for i in range(self.n):
            tmp = sigma.eval(self.field[i]) # raíces de sigma
            if tmp.is_zero():
                roots.append((self.field[i], -i % (len(self.field) - 1))) # potencia a^i que fue raíz => inverso es la posición

        # nanai
        if roots == []:
            raise ValueError()

        # Forney algorithm
        exp = sigma.degree
        coeff = []
        for i in sigma.coefficients: # derivada
            coeff.append(self.field.oproduct(i, exp))
            exp -= 1
        coeff = coeff[:-1] # eliminar el termino cte

        fst = 0 # eliminar ceros anteriores
        for i in range(len(coeff)):
            if coeff[i] == 0:
                fst += 1
            else:
                break
        sigmap = P(coeff[fst:], self.field) # sigma'
        assert(sigmap.degree < sigma.degree)

        # evaluate the error values:
        error = P.zero(self.field)
        for j in roots: # (error, position)
            yj = -self.field.division(omega.eval(j[0]), sigmap.eval(j[0])) #forney
            ej = P([yj] + [self.field.zero()]*j[1], self.field) # error
            error = error + ej # polinomio de errores
        poly = poly + error # recuperar original
        # return codeword
        coeff = poly.coefficients[:-self.nk.degree] # mensaje en los k coeficientes de x^n-1 .. x^n-k
        decode =  P(coeff, self.field) # polinomio asociado
        assert(decode.degree < self.k)

        return decode
