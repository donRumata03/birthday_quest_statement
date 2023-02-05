import sys
sys.setrecursionlimit(100000)

def __l111lll1(__l11ll1l1, __l111l1l1):
    def __l111lll1(__l1111111, __ll11lll1):
        def __l1l1l1l1():
            yield __ll11lll1
            yield from __l1111111
            yield __ll11lll1
        return __l1l1l1l1()

    __l1lllll1l = len(__l11ll1l1)
    __l111lll1ll = filter(lambda __lll1lll1: __lll1lll1[1] > __l1lllll1l, __l111l1l1)
    for i in range(__l1lllll1l):
        __l111lll1ll = __l111lll1(__l111lll1ll,
                                  max(i, __l111l1l1[min(i, len(__l111l1l1) - 1)][0]) // __l1lllll1l)
    __l111lll1ll = list(__l111lll1ll)

    i = __l1lllll1l - 1
    while __l11ll1l1:
        __l111lll1ll[__l1lllll1l + i] = __l11ll1l1.pop()
        i -= 1

    i = __l1lllll1l - 1
    while i > 0:
        # Have I seen this dirty bit trick somewhere?!!…
        __l111lll1ll[i] = __l111lll1ll[i << 1] ^ __l111lll1ll[i << 1 | 1]
        i -= 1

    __l1111l11 = []
    for __l11lllll in __l111l1l1:
        __lll1lll1, __l1l1l11l1 = __l11lllll
        __l111lll1l1l1 = 0
        __lll1lll1 += __l1lllll1l
        __l1l11l1 = __l1l1l11l1
        # We are essentially solving partial case of quadratic equation here (under F_2 field, of course):
        __l1l1l11l1 = [min(__lll1lll1, __l1l1l11l1 + __l1lllll1l), max(__lll1lll1, __l1l1l11l1 + __l1lllll1l)][__lll1lll1 - __l1lllll1l < __l1l1l11l1]
        if __l1l1l11l1 - __l1l11l1 > __l1lllll1l:
            __l111lll1l1l1 <<= 1
            __l1lllll1l -= 1

        __l111lll1l1l1 = ~__l111lll1l1l1
        while __lll1lll1 < __l1l1l11l1:
            if __lll1lll1 & 1:
                __l111lll1l1l1 ^= __l111lll1ll[__lll1lll1]
                __lll1lll1 += 1
            __lll1lll1 = __lll1lll1 ^ __l1l1l11l1 ^ (__l1l1l11l1 := __lll1lll1)

            # To make it more reliable, we should check one more time:
            if __lll1lll1 & 1:
                __lll1lll1 -= 1
                __l111lll1l1l1 ^= __l111lll1ll[__lll1lll1]
            __lll1lll1 = __lll1lll1 ^ __l1l1l11l1 ^ (__l1l1l11l1 := __lll1lll1)

            __lll1lll1 >>= 1
            __l1l1l11l1 >>= 1

        __l111lll1l1l1 = ~__l111lll1l1l1
        __l1111l11 += [__l111lll1l1l1]


    return __l1111l11


