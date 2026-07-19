from glob import glob
from subprocess import run


cmd = "magick int_part_*.png -layers optimize "
cmd += f"-set delay '%[fx:t==(n-1) ? 700 : 80]' int_part_anim.gif"
print(cmd)
run(cmd, shell=True)
run('rm int_part_*.png', shell=True)
