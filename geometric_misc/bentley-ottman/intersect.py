def intersect(p1, p2):
    # This returns the intersection point of given two segments if exists.
    # For tips of the algorithm, we can refer to web page:
    #       https://stackoverflow.com/questions/563198/
    #
    (s1, t1), (s2, t2) = p1, p2
    r = (t1[0] - s1[0], t1[1] - s1[1])
    s = (t2[0] - s2[0], t2[1] - s2[1])

    c = cross_product(*r, *s)
    d = (s2[0] - s1[0], s2[1] - s1[1])
    if c == 0:
        if cross_product(*d, *r) == 0:
            # collinear -> overlapping or disjoint, but we don't treat this
            return (None, None)
        else:
            # parallel -> non-intersecting
            return (None, None)
    else:
        t = float(cross_product(*d, *s)) / c
        u = float(cross_product(*d, *r)) / c
        if 0 <= t and t <= 1 and 0 <= u and u <= 1:
            return (s1[0] + t * r[0], s1[1] + t * r[1])
        else:
            # non-parallel but non-intersection
            return (None, None)


def cross_product(vx, vy, wx, wy):
    # This returns the cross-product (or the outer-product) of
    # given two vectors.
    #
    return vx * wy - vy * wx
