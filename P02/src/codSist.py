from src.polynomial import PolynomialZ2 as poly
# TODO agregar sindromes de las sumas? corrige mas errores
# TODO devolver encode como byte
#       valor hasta 127 => agrega 0 a la izq y al decodificar lo ignorará

# [7, 4, *] - codigos, F(2, 4)
xnk = poly('1000')
# errores
x0 = poly('1')
x1 = poly('10')
x2 = poly('100')
x3 = poly('1000')
x4 = poly('10000')
x5 = poly('100000')
x6 = poly('1000000')

#Cq = <1 + x + x³>
cq = poly('1011')
# Sindromes
s0 = x0.remainder(cq)
s1 = x1.remainder(cq)
s2 = x2.remainder(cq)
s3 = x3.remainder(cq)
s4 = x4.remainder(cq)
s5 = x5.remainder(cq)
s6 = x6.remainder(cq)
# Asoc
scq = {s0: x0, s1: x1, s2: x2, s3: x3, s4: x4, s5: x5, s6: x6}

# Cn = <1 + x^2 + x^3>
cn = poly('1101')
# Sindromes
s0 = x0.remainder(cn)
s1 = x1.remainder(cn)
s2 = x2.remainder(cn)
s3 = x3.remainder(cn)
s4 = x4.remainder(cn)
s5 = x5.remainder(cn)
s6 = x6.remainder(cn)
# Asoc
scn = {s0: x0, s1: x1, s2: x2, s3: x3, s4: x4, s5: x5, s6: x6}

# Codificacion/Decodificacion Sistematica
def encode_msg(mword):
    if mword > 15: # > q^k - 1
        raise Exception("Not a valid message")

    mx = poly(bin(mword))
    aux = xnk.product(mx)
    px = aux.remainder(cq)
    return aux.sum(px).coefficients[0]

def decode_msg(rword):
    if rword > 127: # > q^n - 1
        raise Exception("Not a valid message")

    rx = poly(bin(rword)) # will have an extra zero in left, dropped at init
    sx = rx.remainder(cq)
    if sx.coefficients == [0]:
        return rx.coefficients[0] >> 3
    ex = scq[sx]
    return rx.sum(ex).coefficients[0] >> 3

# test
# cx = encode_msg(10)
# print(cx.str_value())
# sx = decode_msg(115) # correct is 83
# print(sx.str_value())
# sx = decode_msg(83)
# print(sx.str_value())
