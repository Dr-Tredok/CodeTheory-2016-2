from rs import RS
from field import GF
from es import encode_file, decode_file
import sys

# usado en la práctica
gf = GF.primitive()
rs = RS(255, 223, 33, gf)

if len(sys.argv) < 3:
  print("Uso: python3 main.py option input output \n Opciones:\n --encode codifica [file] usando RS(255, 223) al archivo [output]\n --decode decodifica [file] usando RS(255, 223) al archivo [output]")
elif sys.argv[1] == "--encode":
    encode_file(sys.argv[2], sys.argv[3], rs)
elif sys.argv[1] == "--decode":
    decode_file(sys.argv[2], sys.argv[3], rs)
