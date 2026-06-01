from glob import glob
from subprocess import run


cmd = "magick valtr_*.png -layers optimize -delay 30 "
cmd += f"-delay 700 {max(glob('valtr_*.png'))} valtr_anim.gif"
print(cmd)
run(cmd, shell=True)
