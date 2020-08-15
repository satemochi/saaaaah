from glob import glob
from subprocess import run


files = list(glob('cup_game_*.png'))
cmd = 'convert -layers OptimizeFrame -delay 30 cup_game_*.png '
cmd += f'-delay 700 {files[-1]} cup_game_anim1.gif'
print(cmd)
run(cmd, shell=True)
