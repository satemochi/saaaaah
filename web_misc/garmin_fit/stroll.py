from glob import iglob
from itertools import cycle
from subprocess import run
from fitparse import FitFile
import folium


def __get_tours():
    tours = {}
    for i, fit_file in enumerate(iglob('fit/*.FIT')):
        f, lo, la, factor = FitFile(fit_file), [], [], 180 / 0x80000000
        for rec in f.get_messages('record'):
            for data in rec:
                if data.name == 'position_lat':
                    la.append(data.value * factor)
                if data.name == 'position_long':
                    lo.append(data.value * factor)
        tours[i] = lo, la
    return tours


def __get_center(tours):
    cx, cy, n = 0, 0, 0
    for lo, la in tours.values():
        cx += sum(la)
        cy += sum(lo)
        n += len(lo)
    return (cx / n, cy / n)


if __name__ == '__main__':
    t = __get_tours()
    url = 'https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg'
    fmap = folium.Map(location=__get_center(t), tiles=url, zoom_start=14,
                      attr='全国最新写真（シームレス）', width=800, height=800)
    c = cycle(['red', 'blue', 'green', 'purple', 'orange', 'darkred',
               'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
               'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen',
               'gray', 'black', 'lightgray'])
    for lo, la in t.values():
        folium.PolyLine(locations=zip(la, lo), color=next(c)).add_to(fmap)

    fmap.save('xxx.html')
    run('open xxx.html', shell=True)
    run('rm xxx.html', shell=True)
