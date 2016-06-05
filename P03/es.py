#Here is where the magic of reading the files is.

def get_bytes(filename, chunksize = 1):
    with open(filename, "rb") as f:
        chunk = f.read(chunksize) #read the bytes
        while chunk:
            yield chunk #returns the chunk
            chunk = f.read(chunksize) #gets a new chunk from the file

def encode_file(file_to, file_o, code):
    f = open(file_o, 'wb')
    for msg in get_bytes(file_to, code.k):
        codeword = code.encode_bytes(msg)
        f.write(bytes(codeword))
    f.close()
    print("Codificado en " + file_o)

def decode_file(file_to, file_o, code):
    f = open(file_o, 'wb') #reads the encoded file
    for cword in get_bytes(file_to, code.n):
        msg = code.decode_bytes(cword)
        f.write(bytes(msg))
    f.close()
    print("Decodificado en " + file_o)
