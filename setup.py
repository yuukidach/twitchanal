import os
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='twitchanal',
      version='0.1.0',
      author='yuukidach',
      author_email='chendamailbox@foxmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=required,
      python_requires='>=3.7',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      entry_points={'console_scripts': [
          'twitchanal=twitchanal.cli:cli',
      ]})
