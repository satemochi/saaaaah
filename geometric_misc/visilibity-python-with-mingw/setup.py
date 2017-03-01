from distutils.core import setup, Extension

setup(ext_modules=[
    Extension('_visilibity', ['visilibity.i', 'visilibity.cpp'],
              library_dirs=[], libraries=[], extra_compile_args=[],
              extra_link_args=[])])
