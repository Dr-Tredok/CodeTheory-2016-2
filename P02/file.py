import sys

def bytes_from_file(filename, chunksize=1):
    with open(filename, "rb") as f:
        chunk = f.read(chunksize)
        while chunk:
            for b in chunk:
                yield b
            chunk = f.read(chunksize)

for b in bytes_from_file(sys.argv[1]):
    fst = b & 15
    snd = b >> 4
    print(fst)
    print(snd)
