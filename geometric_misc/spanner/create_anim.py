from glob import glob
from os import remove
from os.path import exists
from subprocess import run


files = list(glob('t_spanner_*.png'))
if exists(files[0]):
    print(f'{files[0]} is removed.')
    remove(files[0])

#cmd = 'mogrify -resize 449x449 t_spanner*.png'
cmd = 'mogrify -resize 800x600 t_spanner*.png'
print(cmd)
run(cmd, shell=True)

cmd = 'convert -layers OptimizeFrame -delay 30 t_spanner*.png '
cmd += f'-delay 700 {files[-1]} t_spanner_anim1.gif'
print(cmd)
run(cmd, shell=True)
