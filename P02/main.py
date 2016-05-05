import sys
import src.io as cod

opcion = True if sys.argv[1] == "--encode" else False
polinomio = True if sys.argv[2] == "--cq" else False
archivo = sys.argv[3]

opol = ["Cn", "Cq"]

if opcion:
    print("encoding with ", opol[polinomio], archivo)
    cod.encode_file(archivo, polinomio)
else:
    print("decoding with ", opol[polinomio], archivo)
    cod.decode_file(archivo, polinomio)
