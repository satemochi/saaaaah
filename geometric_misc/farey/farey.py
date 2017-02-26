import matplotlib.pyplot as plt
from fractions import Fraction

n = 4


def draw_circle(x, y, r):
    c = plt.Circle((x, y), r, fill=False, edgecolor='g')
    plt.gcf().gca().add_artist(c)


def farey(x, y, z):
    global n
    if x.denominator + y.denominator <= n:
        farey(x, Fraction(x.numerator + y.numerator,
                          x.denominator + y.denominator), y)
    print y
    r = 1.0 / (2.0 * y.denominator * y.denominator)
    draw_circle(float(y), r, r)
    if y.denominator + z.denominator <= n:
        farey(y, Fraction(y.numerator + z.numerator,
                          y.denominator + z.denominator), z)


def redraw():
    plt.gcf().clf()
    plt.subplot(aspect='equal')
    draw_circle(0, 0.5, 0.5)
    farey(Fraction(0, 1), Fraction(1, 2), Fraction(1, 1))
    draw_circle(1, 0.5, 0.5)
    plt.gcf().canvas.draw()


def press(event):
    global n
    if event.key == 'p':
        n += 1
        redraw()
    elif event.key == 'm':
        n = 0 if n < 0 else n - 1
        redraw()
    elif event.key == 'q':
        plt.savefig('farey.png')
        plt.close()


if __name__ == '__main__':
    fig = plt.figure(facecolor='white')
    fig.canvas.mpl_connect('key_press_event', press)
    redraw()
    plt.show()
