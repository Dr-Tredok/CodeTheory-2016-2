# Sum every term of slist and plist mod prime. Return the list with largest length
def sum_lists(slist, sindex, plist, pindex, prime):
    rindex = max(sindex, pindex)
    result = [0] * (rindex + 1)

    while sindex >= 0 and pindex >= 0:
        result[rindex] = (slist[sindex] + plist[pindex]) % prime
        rindex -= 1
        pindex -= 1
        sindex -= 1

    if sindex > pindex:
        while sindex >= 0:
            result[sindex] = slist[sindex]
            sindex -= 1
    elif pindex > sindex:
        while pindex >= 0:
            result[pindex] = plist[pindex]
            pindex -= 1

    return result

def scprod_list(l, n, p):
    return [(n*x)%p for x in l]

# drop left zeros from a list
def drop_zeros(l):
    # drop 0 not used
    dindex = 0
    length = len(l)

    for j in l:
        if j == 0:
            dindex += 1
        else:
            break

    if dindex == length:
        length = 1
        dindex = -1 # all were 0.. so we get the last
    else:
        length -= dindex

    return l[dindex:], length

# drop left zeros from a string
def drop_str_zeros(string):
    string = string.lstrip('-0b')
    if string == '':
        return '0'
    return string

# xor every term of slist and plist
def xor_lists(slist, index_self, plist, index_poly):
    """ Will xor slist with plist """

    index_p = max([index_self, index_poly])
    length = index_p + 1
    coeff = [0]*(length)

    while index_poly >= 0 and index_self >= 0:
        coeff[index_p] = plist[index_poly] ^ slist[index_self]
        index_poly -= 1
        index_self -= 1
        index_p -= 1

    if index_poly > index_self:
        while index_poly >= 0:
            coeff[index_poly] = plist[index_poly]
            index_poly -= 1
    elif index_self > index_poly:
        while index_self >= 0:
            coeff[index_self] = slist[index_self]
            index_self -= 1

    return coeff, length

# << 1 every term of slist (may be overflow)
def left_shift_list(slist, slength, size):
    coeff = [0] * slength # result

    overflow = 0
    i = slength - 1

    fix_size = 1    # get size bits after shift
    for j in range(1, size):
        fix_size = (fix_size << 1) ^ 1

    while i >= 0:
        coeff[i] = ((slist[i] << 1) & fix_size) ^ overflow
        overflow = (slist[i] >> size - 1) & 1
        i -= 1

    if overflow == 1:
        coeff.insert(0, 1)
        slength+=1

    return coeff, slength
