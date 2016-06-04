from polynomial import *
from field import *

#Here is where the magic of reading the files is.
gf = GF.aes()

def get_bytes(filename, chunksize = 1):
    with open(filename, "rb") as f:
        chunk = f.read(chunksize) #read the bytes
        while chunk:
            yield chunk #returns the chunk
            chunk = f.read(chunksize) #gets a new chunk from the file

def encode_file(file_to, epoly):
    f = open('encode', 'wb')
    for msg in get_bytes(file_to, 223):
        coefficients = [gf.reduce(msg[i]) for i in range(len(msg))]
        poly = Polynomial(coefficients, gf)
        assert(poly.degree < 223)
        f.write(bytes(poly))
    f.close()
    print("Codificado en Code-Decode/encode")

def decode_file(file_to, dpoly):
    f = open('Code-Decode/decode', 'wb') #reads the encoded file
    for byte in get_bytes(file_to):
        pass
    f.close()
    print("Decodificado en Code-Decode/decode")

encode_file("io.py", None)
