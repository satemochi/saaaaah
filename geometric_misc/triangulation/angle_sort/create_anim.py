from glob import glob
from os import remove
from os.path import exists
from subprocess import run


files = list(glob('as_*.png'))
if exists(files[0]):
    print(f'{files[0]} is removed.')
    remove(files[0])

cmd = 'convert -layers OptimizeFrame -delay 30 as_*.png '
cmd += f'-delay 500 {files[-1]} angle_sort_anim.gif'
print(cmd)
run(cmd, shell=True)
