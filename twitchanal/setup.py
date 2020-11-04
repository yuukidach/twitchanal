import os
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='twitchanal',
      version='0.0.1',
      author='yuukidach',
      author_email='chendamailbox@foxmail.com',
      install_requires = required,
      python_requires = '>=3.7',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      entry_points={'console_scripts': [
          'twitchanal=twitchanal.cli:cli',
      ]})
