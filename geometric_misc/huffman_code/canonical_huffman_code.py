from collections import Counter
from functools import reduce
from heapq import heapify, heappop, heappush


def huffman_code(data):
    t, r = _get_tree(_get_heap(Counter(data)))
    codebook, stack = {c: "" for c in data},  [(r, "")]
    while stack:
        c, label = stack.pop()
        _proc(codebook, stack, t[c][0], label+"0")
        _proc(codebook, stack, t[c][1], label+"1")
    return codebook


def _get_tree(q, tree={}):
    while len(q) > 1:
        (ap, al), (bp, bl) = heappop(q), heappop(q)
        heappush(q, (ap+bp, al+bl))
        tree[al+bl] = (al, bl)
    return tree, q[0][1]


def _get_heap(counter):
    q = [(v, k) for k, v in counter.items()]
    heapify(q)
    return q


def _proc(codebook, stack, char, label):
    if char in codebook:
        codebook[char] = label
    else:
        stack.append((char, label))


def canonical_code(hcode):
    ordered = sorted(hcode.items(), key=lambda a: (len(a[1]), a[0]))
    codebook, cval, plen = {}, 0, len(ordered[0][1])
    for c, code in ordered:
        cval <<= (len(code) - plen)
        codebook[c] = str(bin(cval))[2:].zfill(len(code))
        cval, plen = cval+1, len(code)
    return codebook


def encode_codebook(canonical_code):
    bit_count = Counter([len(c) for c in canonical_code.values()])
    bit_lengths = [0] * max(bit_count)
    for k, v in bit_count.items():
        bit_lengths[k-1] = v
    return tuple(bit_lengths), tuple(canonical_code.keys())


def decode_codebook(bit_lens, alphabet):
    al, codebook, cval = list(alphabet)[::-1], {}, 0
    for i, bl in enumerate(bit_lens, 1):
        cval <<= 1
        for j in range(bl):
            codebook[al.pop()] = str(bin(cval)[2:]).zfill(i)
            cval += 1
    return codebook


def encode_string(data, codebook):
    return reduce(lambda s, c: s+codebook[c], data, "")


def decode_string(data, codebook):
    codebook = {v: k for k, v in codebook.items()}
    s, read = "", ""
    for c in data:
        read += c
        if read in codebook:
            s += codebook[read]
            read = ""
    return s


if __name__ == '__main__':
    from pprint import pprint
    s = "Hello world."
    s = "Hello hello, hello world."
    # s = "Hello hello, hello world................"
    s = "aaabbaaacdcdaaabbbzzzz"
    print(f'\n\n--------------\nInput string: {s}\n')
    code = huffman_code(s)
    print('Huffman code:')
    pprint(code)
    print('~~~~~~~~~~~~~~')
    cc = canonical_code(code)
    pprint(cc)
    bl, a = encode_codebook(cc)
    print('\n')
    print(bl)
    print(a, '\n')
    dcc = decode_codebook(bl, a)
    pprint(dcc)
    print(encode_string(s, dcc))
    print(decode_string(encode_string(s, dcc), dcc))
