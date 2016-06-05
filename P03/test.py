from polynomial import *
from field import *
from rs import *

def roman():
    f = GF.roman()
    rs = RS(15, 11, 5, f)
    # palabra recibida con errores
    rx = Polynomial([f.unity()] +  [f.zero()]*3 + [f.unity()]*3 + [f.zero()]*5 + [f.unity()], f)
    print(rx)
    # mensaje recibido
    mx = rs.decode(rx)
    print(mx)
    # palabra decodificada
    sx = rs.encode(mx)
    print(sx)

def p03():
    f = GF.primitive()
    rs = RS(255, 223, 33, f)
    # x^220 + a^2 x^200 + a^1 x^16 + a^5 x^15 + a^4 x^14 + a^1 x^1 + a^100
    mx = Polynomial([f[0]] + [f.zero()]*19 + [f[2]] + [f.zero()]*183 + [f[1], f[5], f[4]] + [f.zero()]*12 + [f[1], f[100]], f)
    print("Mensaje original: ")
    print(mx)
    # x^252 + a^2 x^232 + a^1 x^48 + a^5 x^47 + a^4 x^46 + a^1 x^33 + a^100 x^32 + p(x)
    cx = rs.encode(mx)
    print("Codificada: ")
    print(cx)
    # a^3 x^49 + a^50 x^15
    ex = Polynomial([f[3]] + [f.zero()]*49, f) + Polynomial([f[50]] + [f.zero()]*15, f)
    print("Errores: ")
    print(ex)
    # x^252 + a^2 x^232 + a^3 x^49 + a^1 x^48 + a^5 x^47 + a^4 x^46 + a^1 x^33 + a^100 x^32 + p'(x)
    rx = cx + ex
    print("Recibida: ")
    print(rx)
    # Decodificada, debe ser igual a mx
    sx = rs.decode(rx)
    print("Decodificada: ")
    print(sx)
    assert(sx == mx)
