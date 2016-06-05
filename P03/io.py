from polynomial import *
from field import *
from rs import *

#Here is where the magic of reading the files is.
gf = GF.primitive()
rs = RS(255, 223, 33, gf)

def get_bytes(filename, chunksize = 1):
    with open(filename, "rb") as f:
        chunk = f.read(chunksize) #read the bytes
        while chunk:
            yield chunk #returns the chunk
            chunk = f.read(chunksize) #gets a new chunk from the file

def encode_file(file_to):
    f = open('encode', 'wb')
    for msg in get_bytes(file_to, rs.k):
        codeword = rs.encode(msg)
        f.write(bytes(codeword))
    f.close()
    print("Codificado en Code-Decode/encode")

def decode_file(file_to):
    f = open('decode', 'wb') #reads the encoded file
    for cword in get_bytes(file_to, rs.n):
        msg = rs.decode(cword)
        f.write(bytes(msg))
    f.close()
    print("Decodificado en Code-Decode/decode")

#encode_file("io.py")
decode_file("dec")
