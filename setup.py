from distutils.core import setup
from glob import glob
from setuptools import find_packages


"""
This is a setup for Travis. There are more details that can be added in this setup, but these are the ones I think are essential. 
They say where the source files are. 
"""

setup(
      packages=find_packages('PsyGuideSite'),
      package_dir={'': 'PsyGuideSite'},
     )
