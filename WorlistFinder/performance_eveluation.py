# def test_set(xs):
def check_dup_set(xs):
    seen = set()  # O(1) lookups
    for x in xs:
        if x not in seen:
            seen.add(x)
        else:
            return True

    return False

import collections

# def test_counter(xs):
def check_dup_counter(xs):
    freq = collections.Counter(xs)
    for k in freq:
        if freq[k] > 1:
            return True

    return False

# def test_dict(xs):
def check_dup_dict(xs):
    d = {}
    for x in xs:
        if x in d:
            return True
        d[x] = 1

    return False

# def test_sort(xs):
def check_dup_sort(xs):
    ys = sorted(xs)

    for n in range(1, len(xs)):
        if ys[n] == ys[n-1]:
            return True

    return False

##

# import sys, timeit
# print (sys.version + "\n")
# xs = list(range(10000)) + [999]
# fns = [p for name, p in globals().items() if name.startswith('check_dup')]
# for fn in fns:
#     print ('%50s %.5f' % (fn, timeit.timeit(lambda: fn(xs), number=100)))