#! /bin/sh
iperender -png -resolution 300 lp_formula.pdf lp_formula.png
pyreverse -o png -fALL tsp.py
