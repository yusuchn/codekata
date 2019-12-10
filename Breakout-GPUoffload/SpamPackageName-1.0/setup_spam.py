# both setuptools and distutils doing the similar things,
# both working in this case
# from setuptools import setup, find_packages
from setuptools import setup, Extension
# from distutils.core import setup, Extension

# # Load Version
# exec(open('./prior_pipeline/_version.py', 'r').read())
moduleSpam = Extension('spam',
                   sources = ['spammodule.c'])

setup(name='SpamPackageName',
    description='This is a tutorial package',
    version='1.0',
    author="Tutorial",
    ext_modules = [moduleSpam])

