def accel_asc(n):
    """ Kelleher & O'Sullivan (2014):
            "Generating All Partitions: A Comparison Of Two Encodings",
            https://arxiv.org/abs/0909.2331
    """
    a, y, k = [1] * n, -1, n
    while k > 0:
        k -= 1
        x = a[k] + 1
        while (x << 1) <= y:
            a[k], y = x, y - x
            k += 1
        ell = k + 1
        while x <= y:
            a[k], a[ell] = x, y
            yield a[:ell + 1]
            x, y = x+1, y-1
        a[k] = x + y
        yield a[:ell]
        y += x - 1


class box:
    def __init__(self, parts):
        self.__parts = parts

    @property
    def n(self):
        return sum(self.__parts)

    def draw(self):
        title = f"{self.n} = " + ' + '.join(str(i) for i in self.__parts)
        plt.gca().set_title(title, loc='left')
        for x, val in enumerate(self.__parts):
            for y in range(val):
                fc = colors.to_rgba(f'C{val}', 0.3)
                sqr = patches.Polygon([(x, y), (x+1, y), (x+1, y+1), (x, y+1)],
                                      closed=True, facecolor=fc,
                                      edgecolor='k', linewidth=2)
                plt.gca().add_patch(sqr)


if __name__ == '__main__':
    from matplotlib import colors, patches, pyplot as plt

    plt.tight_layout()
    for i, p in enumerate(accel_asc((n := 11))):
        print(p)
        plt.cla()
        plt.gca().set_xlim(0, n+1)
        plt.gca().set_ylim(0, n+1)
        plt.gca().set_aspect('equal')
        box(p).draw()
        plt.draw()
        # plt.savefig(f'int_part_{str(i).zfill(3)}.png', dpi=200)
        plt.pause(0.1)
    plt.show()
