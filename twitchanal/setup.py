from setuptools import setup, find_packages

setup(
    name='twitchanal',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'console_scripts':[
            'twitchanal=twitchanal.cli:cli',
        ]
    }
)