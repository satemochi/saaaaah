from glob import glob
from os.path import basename
from subprocess import run


for f in (files := glob('*.py')):
    if f == basename(__file__):
        continue
    print(f"python {f}")
    run(["python", f"{f}"])
