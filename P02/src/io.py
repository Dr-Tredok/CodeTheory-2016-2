from . import codSist as c

#Here is where the magic of reading the files is.

def get_bytes(filename, chunksize = 1):
    with open(filename, "rb") as f:
        chunk = f.read(chunksize) #read the byte
        while chunk:
            yield chunk #returns the chunk
            chunk = f.read(chunksize) #gets a new chunk from the file

# System In (where it takes the bytes and bits and mushes then into the coder)
def encode_file(file_to, epoly):
    f = open('Code-Decode/encode', 'wb')
    for byte in get_bytes(file_to):
        b = int.from_bytes(byte, byteorder = 'big')
        fst = b & 15
        snd = b >> 4 #takes 4 bits
        fstx = c.encode_msg(fst, epoly)
        sndx = c.encode_msg(snd, epoly)

        f.write(sndx.to_bytes(1, byteorder = "big"))
        f.write(fstx.to_bytes(1, byteorder = "big"))
    f.close()
    print("Codificado en Code-Decode/encode")

def decode_file(file_to, dpoly):
    #System out each byte has to generate two (and will)
    f = open('Code-Decode/decode', 'wb') #reads the encoded file
    for byte in get_bytes(file_to, 2):
        i = 0
        for b in byte:
            dec = c.decode_msg(b, dpoly)
            i = (i << 4) ^ dec
        f.write(i.to_bytes(1, byteorder="big"))
    f.close()
    print("Decodificado en Code-Decode/decode")
