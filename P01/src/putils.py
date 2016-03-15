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

def drop_zeros(l):
    # drop 0 not used
    dindex = 0
    for j in l:
        if j == 0:
            dindex += 1
        else:
            break
    if dindex == len(l):
        dindex = -1 # all were 0.. so we get the last

    return l[dindex:]
