import math

__author__ = 'Roman'

def correlation(log1, log2, dictionary):
    log1Set = set()
    for word in log1["MESSAGE"].split(" "):
        log1Set.add(word)

    log2Set = set()
    for word in log2["MESSAGE"].split(" "):
        log2Set.add(word)

    p00 = 0
    p01 = 0
    p10 = 0
    p11 = 0

    for word in dictionary:
        if word in log1Set and word in log2Set:
            p11 += 1
        elif word in log1Set and not word in log2Set:
            p01 += 1
        elif not word in log1Set and word in log2Set:
            p10 += 1
        elif not word in log1Set and not word in log2Set:
            p00 += 1

    p0plus = p00 + p01
    p1plus = p10 + p11
    pplus0 = p00 + p10
    pplus1 = p01 + p11

    corr = (p00 * p11 - p01 * p10) / math.sqrt(p0plus * p1plus * pplus0 * pplus1)
    return corr