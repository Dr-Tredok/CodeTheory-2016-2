#Here is where the magic of reading the files is. 
import sys
import src.codSist as c

def get_bytes(filename, chunksize = 1):
    with open(filename, "rb") as f:
        chunk = f.read(chunksize) #read the byte
        while chunk:
            yield chunk #returns the chunk
            chunk = f.read(chunksize) #gets a new chunk from the file

# System In (where it takes the bytes and bits and mushes then into the coder)
f = open('tmp.txt', 'wb')
for byte in get_bytes(sys.argv[1]):
    b = int.from_bytes(byte, byteorder = 'big')
    fst = b & 15 
    snd = b >> 4 #takes 4 bits
    fstx = c.encode_msg(fst) 
    sndx = c.encode_msg(snd)
    
    f.write(sndx-to_bytes(1, byteorder = "big"))
    f.write(fstx.to_bytes(1, byteorder = "big"))
f.close()

    #System out each byte has to generate two (and will)
    f = open('tmpd.txt', 'wb') #reads the encoded file
    for byte in get_bytes("tmp.txt", 2):
        i = 0
        for b in byte:
            dec = c.decode_msg(b)
            i = (i << 4) ^ dec
        f.write(i.to_bytes(1, byteorder="big"))
f.close()
