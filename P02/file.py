import sys
import src.codSist as c

def bytes_from_file(filename, chunksize=1):
    with open(filename, "rb") as f:
        chunk = f.read(chunksize)
        while chunk:
            yield chunk
            chunk = f.read(chunksize)

# encode
f = open('tmp.txt', 'wb')
for byte in bytes_from_file(sys.argv[1]):
    b = int.from_bytes(byte, byteorder='big')
    fst = b & 15
    snd = b >> 4
    fstx = c.encode_msg(fst)
    sndx = c.encode_msg(snd)

    f.write(sndx.to_bytes(1, byteorder="big"))
    f.write(fstx.to_bytes(1, byteorder="big"))
f.close()

# decode.. each byte generate two
f = open('tmpd.txt', 'wb')
for byte in bytes_from_file("tmp.txt", 2):
    i = 0
    for b in byte:
        dec = c.decode_msg(b)
        i = (i << 4) ^ dec
    f.write(i.to_bytes(1, byteorder="big"))
f.close()
