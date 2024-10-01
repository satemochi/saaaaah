def stanley_sequence(n=40):
    """ return 3-AP-Free (sub)set of {0, ..., n} """
    return [i for i in range(n+1) if __st(i)]


def __st(x):
    while x:
        x, r = divmod(x, 3)
        if r not in (_ := (0, 1)):
            return False
    return True


if __name__ == '__main__':
    print(a := stanley_sequence())
    for i in a:
        print(i, bin(i))
