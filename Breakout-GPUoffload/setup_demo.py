# from distutils.core import setup, Extension
from setuptools import setup, Extension

moduleDemo = Extension('xyzzy',
                    sources = ['demo.c'])

setup (name = 'DemoPackageName',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [moduleDemo])